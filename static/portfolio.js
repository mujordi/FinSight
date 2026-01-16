/**
 * Portfolio Management
 * Handles adding, removing, and displaying portfolio products
 */

const Portfolio = {
  products: [],
  pieChart: null,
  currentView: 'product', // 'product' or 'type'

  init() {
    this.loadPortfolio();
    this.setupEventListeners();
  },

  setupEventListeners() {
    // Add product
    const addBtn = document.getElementById('add-product-btn');
    if (addBtn) {
      addBtn.addEventListener('click', (e) => {
        e.preventDefault();
        this.addProduct();
      });
    }

    // CSV Upload
    const csvUpload = document.getElementById('csv-upload');
    if (csvUpload) {
      csvUpload.addEventListener('change', (e) => {
        this.handleCSVUpload(e);
      });
    }

    // Export CSV
    const exportBtn = document.getElementById('export-csv-btn');
    if (exportBtn) {
      exportBtn.addEventListener('click', (e) => {
        e.preventDefault();
        this.exportCSV();
      });
    }

    // Also handle Enter key on form inputs
    ['product-name', 'product-ticker', 'product-percentage'].forEach(id => {
      const input = document.getElementById(id);
      if (input) {
        input.addEventListener('keypress', (e) => {
          if (e.key === 'Enter') {
            e.preventDefault();
            this.addProduct();
          }
        });
      }
    });

    // View toggle buttons
    const viewProductBtn = document.getElementById('view-by-product');
    const viewTypeBtn = document.getElementById('view-by-type');
    
    if (viewProductBtn) {
      viewProductBtn.addEventListener('click', () => {
        this.switchView('product');
      });
    }
    
    if (viewTypeBtn) {
      viewTypeBtn.addEventListener('click', () => {
        this.switchView('type');
      });
    }
  },

  switchView(view) {
    this.currentView = view;
    
    const productView = document.getElementById('product-view');
    const typeView = document.getElementById('type-view');
    const productBtn = document.getElementById('view-by-product');
    const typeBtn = document.getElementById('view-by-type');
    
    if (view === 'product') {
      productView.style.display = 'block';
      typeView.style.display = 'none';
      productBtn.classList.add('active');
      typeBtn.classList.remove('active');
    } else {
      productView.style.display = 'none';
      typeView.style.display = 'block';
      productBtn.classList.remove('active');
      typeBtn.classList.add('active');
      this.renderTypeView();
    }
  },

  async loadPortfolio() {
    try {
      const response = await fetch('/api/portfolio', {
        credentials: 'include' // Important for cookies!
      });
      
      console.log('Load portfolio response:', response.status);
      
      if (response.ok) {
        const data = await response.json();
        console.log('Portfolio loaded:', data);
        this.products = data.products || [];
        this.render();
      } else {
        console.error('Error loading portfolio:', response.status);
      }
    } catch (error) {
      console.error('Error loading portfolio:', error);
    }
  },

  async addProduct() {
    const nameEl = document.getElementById('product-name');
    const tickerEl = document.getElementById('product-ticker');
    const percentageEl = document.getElementById('product-percentage');

    if (!nameEl || !percentageEl) {
      console.error('Form elements not found');
      return;
    }

    const name = nameEl.value.trim();
    const ticker = tickerEl ? tickerEl.value.trim() : '';
    const percentage = parseFloat(percentageEl.value);

    console.log('Adding product:', { name, ticker, percentage });

    if (!name || !percentage || percentage <= 0) {
      alert('Please enter product name and valid percentage');
      return;
    }

    try {
      const response = await fetch('/api/portfolio/add', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        credentials: 'include', // Important for cookies!
        body: JSON.stringify({ name, ticker, percentage })
      });

      console.log('Response status:', response.status);

      if (response.ok) {
        const product = await response.json();
        console.log('Product added:', product);
        this.products.push(product);
        this.render();
        
        // Clear form
        nameEl.value = '';
        if (tickerEl) tickerEl.value = '';
        percentageEl.value = '';
        
        // Show success
        alert('Product added successfully!');
      } else {
        const error = await response.json();
        console.error('Error response:', error);
        alert('Error adding product: ' + (error.error || 'Unknown error'));
      }
    } catch (error) {
      console.error('Error adding product:', error);
      alert('Error adding product: ' + error.message);
    }
  },

  async removeProduct(productId) {
    if (!confirm('Remove this product from portfolio?')) return;

    try {
      const response = await fetch(`/api/portfolio/remove/${productId}`, {
        method: 'DELETE'
      });

      if (response.ok) {
        this.products = this.products.filter(p => p.id !== productId);
        this.render();
      }
    } catch (error) {
      console.error('Error removing product:', error);
    }
  },

  async handleCSVUpload(event) {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/portfolio/import-csv', {
        method: 'POST',
        body: formData
      });

      if (response.ok) {
        const result = await response.json();
        alert(`Imported ${result.added} products successfully!`);
        this.loadPortfolio();
      } else {
        alert('Error importing CSV');
      }
    } catch (error) {
      console.error('Error importing CSV:', error);
      alert('Error importing CSV');
    }

    // Reset input
    event.target.value = '';
  },

  exportCSV() {
    if (this.products.length === 0) {
      alert('No products to export');
      return;
    }

    // Create CSV content
    const headers = ['name', 'ticker', 'type', 'model', 'percentage'];
    const rows = this.products.map(p => [
      p.name,
      p.ticker,
      p.type,
      p.model,
      p.percentage
    ]);

    let csv = headers.join(',') + '\n';
    rows.forEach(row => {
      csv += row.map(field => `"${field}"`).join(',') + '\n';
    });

    // Download
    const blob = new Blob([csv], { type: 'text/csv' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'portfolio.csv';
    a.click();
    window.URL.revokeObjectURL(url);
  },

  render() {
    this.renderTable();
    this.renderDistribution();
    this.renderPieChart();
    if (this.currentView === 'type') {
      this.renderTypeView();
    }
  },

  renderTable() {
    const tbody = document.getElementById('portfolio-tbody');
    if (!tbody) return;

    if (this.products.length === 0) {
      tbody.innerHTML = `
        <tr class="empty-state">
          <td colspan="6" style="text-align: center; padding: 2rem; color: var(--text-secondary);">
            No products yet. Add your first product above! 👆
          </td>
        </tr>
      `;
      return;
    }

    tbody.innerHTML = this.products.map(product => `
      <tr>
        <td><strong>${product.name}</strong></td>
        <td>${product.ticker || '-'}</td>
        <td><span class="badge-type">${product.type}</span></td>
        <td><span class="badge-model">${product.model}</span></td>
        <td><strong>${product.percentage.toFixed(2)}%</strong></td>
        <td>
          <button class="btn-delete" onclick="Portfolio.removeProduct('${product.id}')">🗑️</button>
        </td>
      </tr>
    `).join('');
  },

  renderDistribution() {
    const distribution = {};
    let total = 0;

    // Calculate distribution
    this.products.forEach(product => {
      const model = product.model;
      distribution[model] = (distribution[model] || 0) + product.percentage;
      total += product.percentage;
    });

    // Update cards
    const cards = document.querySelectorAll('.distribution-card');
    cards.forEach(card => {
      const model = card.dataset.model;
      const percentage = distribution[model] || 0;
      const percentageEl = card.querySelector('.model-percentage');
      
      if (percentageEl) {
        percentageEl.textContent = percentage.toFixed(1) + '%';
      }

      // Highlight if has allocation
      if (percentage > 0) {
        card.classList.add('active');
      } else {
        card.classList.remove('active');
      }
    });

    // Update total
    const totalEl = document.getElementById('total-allocation');
    if (totalEl) {
      const totalStrong = totalEl.querySelector('strong');
      if (totalStrong) {
        totalStrong.textContent = total.toFixed(1) + '%';
        // Color code based on total
        if (Math.abs(total - 100) < 0.1) {
          totalStrong.style.color = 'var(--green)';
        } else if (total > 100) {
          totalStrong.style.color = 'var(--red)';
        } else {
          totalStrong.style.color = 'var(--yellow)';
        }
      }
    }
  },

  renderTypeView() {
    const tbody = document.getElementById('type-tbody');
    if (!tbody) return;

    if (this.products.length === 0) {
      tbody.innerHTML = `
        <tr class="empty-state">
          <td colspan="4" style="text-align: center; padding: 2rem; color: var(--text-secondary);">
            No products yet.
          </td>
        </tr>
      `;
      return;
    }

    // Group by type
    const typeGroups = {};
    this.products.forEach(product => {
      const type = product.type;
      if (!typeGroups[type]) {
        typeGroups[type] = {
          count: 0,
          percentage: 0,
          products: []
        };
      }
      typeGroups[type].count++;
      typeGroups[type].percentage += product.percentage;
      typeGroups[type].products.push(product.name);
    });

    // Render table
    tbody.innerHTML = Object.entries(typeGroups)
      .sort((a, b) => b[1].percentage - a[1].percentage)
      .map(([type, data]) => `
        <tr>
          <td><strong><span class="badge-type">${type}</span></strong></td>
          <td>${data.count}</td>
          <td><strong>${data.percentage.toFixed(2)}%</strong></td>
          <td style="font-size: 0.85rem; color: var(--text-secondary);">
            ${data.products.slice(0, 3).join(', ')}${data.products.length > 3 ? '...' : ''}
          </td>
        </tr>
      `).join('');
  },

  renderPieChart() {
    const canvas = document.getElementById('type-pie-chart');
    if (!canvas) return;

    if (this.products.length === 0) {
      if (this.pieChart) {
        this.pieChart.destroy();
        this.pieChart = null;
      }
      return;
    }

    // Calculate distribution by type
    const typeDistribution = {};
    this.products.forEach(product => {
      const type = product.type;
      typeDistribution[type] = (typeDistribution[type] || 0) + product.percentage;
    });

    // Sort by percentage
    const sortedTypes = Object.entries(typeDistribution)
      .sort((a, b) => b[1] - a[1]);

    const labels = sortedTypes.map(([type]) => type);
    const data = sortedTypes.map(([, percentage]) => percentage);

    // Color palette
    const colors = [
      '#3b82f6', // Blue
      '#22c55e', // Green
      '#eab308', // Yellow
      '#ef4444', // Red
      '#8b5cf6', // Purple
      '#ec4899', // Pink
      '#14b8a6', // Teal
      '#f97316', // Orange
      '#6366f1', // Indigo
      '#84cc16', // Lime
    ];

    // Create or update chart
    if (this.pieChart) {
      this.pieChart.data.labels = labels;
      this.pieChart.data.datasets[0].data = data;
      this.pieChart.update();
    } else {
      this.pieChart = new Chart(canvas, {
        type: 'pie',
        data: {
          labels: labels,
          datasets: [{
            data: data,
            backgroundColor: colors.slice(0, labels.length),
            borderColor: '#1e293b',
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: true,
          plugins: {
            legend: {
              position: 'right',
              labels: {
                color: '#f1f5f9',
                font: {
                  size: 12
                },
                padding: 15,
                generateLabels: function(chart) {
                  const data = chart.data;
                  if (data.labels.length && data.datasets.length) {
                    return data.labels.map((label, i) => {
                      const value = data.datasets[0].data[i];
                      return {
                        text: `${label}: ${value.toFixed(1)}%`,
                        fillStyle: data.datasets[0].backgroundColor[i],
                        hidden: false,
                        index: i
                      };
                    });
                  }
                  return [];
                }
              }
            },
            tooltip: {
              callbacks: {
                label: function(context) {
                  return `${context.label}: ${context.parsed.toFixed(2)}%`;
                }
              }
            }
          }
        }
      });
    }
  }
};

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => Portfolio.init());
} else {
  Portfolio.init();
}

