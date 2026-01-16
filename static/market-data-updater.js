// FinSight - Market Data Updater
// Fetches real-time market data and updates tables

const MarketDataUpdater = {
  // Configuration
  config: {
    refreshInterval: 60000, // 60 seconds
    apiBaseUrl: '/api/market-data',
    tabDataSources: {
      'macro': 'macro',
      'gold': 'gold',
      'equities': 'equities',
      'crypto': 'crypto',
      'fixedincome': 'fixed-income',
      'thematic': 'thematic',
      'growth': 'growth',
      'highbeta': 'highbeta'
    }
  },

  // Cache for data
  cache: {},
  lastUpdate: null,
  refreshTimer: null,

  // Format value based on type
  formatValue(value, key) {
    if (value === null || value === undefined) {
      return 'N/A';
    }

    // Different formatting based on the data type
    if (key.includes('yield') || key === 'inflation' || key === 'real_yields') {
      // Yields and rates as percentage
      return `${value.toFixed(2)}%`;
    } else if (key === 'valuations') {
      // P/E ratio
      return `${value.toFixed(1)}x`;
    } else if (value > 1000) {
      // Large numbers with comma separator
      return new Intl.NumberFormat('en-US', {
        minimumFractionDigits: 0,
        maximumFractionDigits: 0
      }).format(value);
    } else if (value > 100) {
      // Medium numbers with 2 decimals
      return value.toFixed(2);
    } else {
      // Small numbers with 2-4 decimals
      return value.toFixed(value < 10 ? 3 : 2);
    }
  },

  // Create change indicator HTML
  createChangeIndicator(change) {
    if (!change || change === 0) {
      return '';
    }

    const isPositive = change > 0;
    const arrow = isPositive ? '▲' : '▼';
    const className = isPositive ? 'change-up' : 'change-down';
    const sign = isPositive ? '+' : '';
    
    return `<span class="change-indicator ${className}">${arrow} ${sign}${change.toFixed(2)}%</span>`;
  },

  // Update a single cell
  updateCell(cell, data) {
    const key = cell.getAttribute('data-key');
    if (!data[key]) return;

    const { value, change } = data[key];
    const formattedValue = this.formatValue(value, key);
    const changeIndicator = this.createChangeIndicator(change);

    cell.innerHTML = `
      <span class="value-number">${formattedValue}</span>
      ${changeIndicator}
    `;
    cell.classList.remove('loading');
    cell.classList.add('loaded');
  },

  // Update all cells in a tab
  async updateTab(tabId) {
    const dataSource = this.config.tabDataSources[tabId];
    if (!dataSource) return;

    try {
      // Check cache first (5 second freshness)
      const now = Date.now();
      if (this.cache[dataSource] && (now - this.cache[dataSource].timestamp < 5000)) {
        this.applyDataToTab(tabId, this.cache[dataSource].data);
        return;
      }

      // Fetch from API
      const response = await fetch(`${this.config.apiBaseUrl}/${dataSource}`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      
      const data = await response.json();
      
      // Update cache
      this.cache[dataSource] = {
        data: data,
        timestamp: now
      };

      // Apply data to tab
      this.applyDataToTab(tabId, data);
      
    } catch (error) {
      console.error(`Error fetching data for ${tabId}:`, error);
      this.showError(tabId);
    }
  },

  // Apply data to tab cells
  applyDataToTab(tabId, data, signals = null) {
    const tab = document.getElementById(tabId);
    if (!tab) return;

    // Find all value cells in this tab
    const valueCells = tab.querySelectorAll('.value-cell');
    
    valueCells.forEach(cell => {
      const dataSourceAttr = cell.getAttribute('data-source');
      
      // If cell specifies a different data source (e.g., macro data in another tab)
      if (dataSourceAttr) {
        this.fetchAndUpdateCell(cell, dataSourceAttr);
      } else {
        this.updateCell(cell, data);
      }
    });

    // Update signal, weight, and explanation cells if signals are provided
    if (signals && signals[tabId]) {
      this.updateSignalCells(tab, signals[tabId]);
    }
  },

  // Update signal, weight, and explanation cells
  updateSignalCells(tab, signals) {
    const signalCells = tab.querySelectorAll('.signal-cell');
    const weightCells = tab.querySelectorAll('.weight-cell');
    const explanationCells = tab.querySelectorAll('.explanation-cell');

    signalCells.forEach(cell => {
      const key = cell.getAttribute('data-key');
      if (signals[key]) {
        const signal = signals[key].signal;
        // Remove old classes
        cell.classList.remove('red', 'yellow', 'green');
        // Add new class based on signal
        if (signal === 'positive') {
          cell.classList.add('green');
          cell.textContent = 'Positive';
        } else if (signal === 'negative') {
          cell.classList.add('red');
          cell.textContent = 'Negative';
        } else {
          cell.classList.add('yellow');
          cell.textContent = 'Neutral';
        }
      }
    });

    weightCells.forEach(cell => {
      const key = cell.getAttribute('data-key');
      if (signals[key]) {
        const weight = signals[key].weight;
        cell.textContent = weight.charAt(0).toUpperCase() + weight.slice(1);
      }
    });

    explanationCells.forEach(cell => {
      const key = cell.getAttribute('data-key');
      if (signals[key]) {
        cell.textContent = signals[key].explanation;
      }
    });
  },

  // Fetch data for a specific cell with different source
  async fetchAndUpdateCell(cell, dataSource) {
    try {
      const now = Date.now();
      
      // Check cache
      if (this.cache[dataSource] && (now - this.cache[dataSource].timestamp < 5000)) {
        this.updateCell(cell, this.cache[dataSource].data);
        return;
      }

      // Fetch from API
      const response = await fetch(`${this.config.apiBaseUrl}/${dataSource}`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      
      const data = await response.json();
      
      // Update cache
      this.cache[dataSource] = {
        data: data,
        timestamp: now
      };

      this.updateCell(cell, data);
      
    } catch (error) {
      console.error(`Error fetching data from ${dataSource}:`, error);
    }
  },

  // Show error state
  showError(tabId) {
    const tab = document.getElementById(tabId);
    if (!tab) return;

    const cells = tab.querySelectorAll('.value-cell.loading');
    cells.forEach(cell => {
      cell.innerHTML = '<span class="error">Error</span>';
      cell.classList.remove('loading');
    });
  },

  // Update all data
  async updateAllData() {
    try {
      const response = await fetch(`${this.config.apiBaseUrl}/all`);
      if (!response.ok) throw new Error(`HTTP ${response.status}`);
      
      const allData = await response.json();
      this.lastUpdate = new Date(allData.last_update);

      // Extract signals if present
      const signals = allData.signals || {};

      // Update cache for all data sources
      Object.keys(this.config.tabDataSources).forEach(tabId => {
        const dataSource = this.config.tabDataSources[tabId];
        const dataKey = dataSource.replace('-', '_');
        
        if (allData[dataKey]) {
          this.cache[dataSource] = {
            data: allData[dataKey],
            timestamp: Date.now()
          };
          this.applyDataToTab(tabId, allData[dataKey], signals);
        }
      });

      // Update last update indicator
      this.updateLastUpdateIndicator();
      
    } catch (error) {
      console.error('Error fetching all data:', error);
    }
  },

  // Update last update indicator in UI
  updateLastUpdateIndicator() {
    const indicator = document.getElementById('last-update');
    if (indicator && this.lastUpdate) {
      const timeStr = this.lastUpdate.toLocaleTimeString('en-US', {
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit'
      });
      indicator.textContent = `Last update: ${timeStr}`;
      indicator.classList.add('updated');
      
      setTimeout(() => {
        indicator.classList.remove('updated');
      }, 1000);
    }
  },

  // Start auto-refresh
  startAutoRefresh() {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer);
    }

    this.refreshTimer = setInterval(() => {
      this.updateAllData();
    }, this.config.refreshInterval);
  },

  // Stop auto-refresh
  stopAutoRefresh() {
    if (this.refreshTimer) {
      clearInterval(this.refreshTimer);
      this.refreshTimer = null;
    }
  },

  // Manual refresh trigger
  manualRefresh() {
    // Clear cache to force fresh data
    this.cache = {};
    this.updateAllData();
  },

  // Initialize
  init() {
    console.log('Initializing Market Data Updater...');
    
    // Initial data load
    this.updateAllData();

    // Start auto-refresh
    this.startAutoRefresh();

    // Listen for tab changes to load data for that tab
    document.addEventListener('tabChanged', (e) => {
      const tabId = e.detail?.tabId;
      if (tabId) {
        this.updateTab(tabId);
      }
    });

    // Add manual refresh button listener if exists
    const refreshBtn = document.getElementById('refresh-data-btn');
    if (refreshBtn) {
      refreshBtn.addEventListener('click', () => {
        this.manualRefresh();
      });
    }

    console.log('Market Data Updater initialized successfully');
  }
};

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', () => {
    MarketDataUpdater.init();
  });
} else {
  MarketDataUpdater.init();
}

// Export for global use
window.MarketDataUpdater = MarketDataUpdater;

