// FinSight Charts - Chart.js Implementation
// Modern, interactive charts with time range selection

// Mock data generator for demo purposes
function generateMockData(days, baseValue, volatility = 0.02) {
  const data = [];
  const now = new Date();
  let value = baseValue;
  
  for (let i = days; i >= 0; i--) {
    const date = new Date(now);
    date.setDate(date.getDate() - i);
    
    // Random walk with trend
    const change = (Math.random() - 0.48) * volatility * value;
    value = Math.max(value + change, baseValue * 0.5); // Prevent going too low
    
    data.push({
      x: date,
      y: parseFloat(value.toFixed(2))
    });
  }
  
  return data;
}

// Chart configuration presets
const chartDefaults = {
  responsive: true,
  maintainAspectRatio: false,
  interaction: {
    mode: 'index',
    intersect: false,
  },
  plugins: {
    legend: {
      display: false
    },
    tooltip: {
      backgroundColor: 'rgba(15, 23, 42, 0.95)',
      titleColor: '#f1f5f9',
      bodyColor: '#94a3b8',
      borderColor: '#334155',
      borderWidth: 1,
      padding: 12,
      displayColors: false,
      callbacks: {
        title: function(context) {
          const date = new Date(context[0].parsed.x);
          return date.toLocaleDateString('en-US', { 
            month: 'short', 
            day: 'numeric', 
            year: 'numeric' 
          });
        },
        label: function(context) {
          let label = context.dataset.label || '';
          if (label) {
            label += ': ';
          }
          label += new Intl.NumberFormat('en-US', {
            style: 'decimal',
            minimumFractionDigits: 2,
            maximumFractionDigits: 2
          }).format(context.parsed.y);
          return label;
        }
      }
    }
  },
  scales: {
    x: {
      type: 'time',
      time: {
        unit: 'day',
        displayFormats: {
          day: 'MMM d',
          week: 'MMM d',
          month: 'MMM yyyy'
        }
      },
      grid: {
        color: 'rgba(51, 65, 85, 0.3)',
        drawBorder: false
      },
      ticks: {
        color: '#64748b',
        maxRotation: 0,
        autoSkipPadding: 20
      }
    },
    y: {
      position: 'right',
      grid: {
        color: 'rgba(51, 65, 85, 0.3)',
        drawBorder: false
      },
      ticks: {
        color: '#64748b',
        callback: function(value) {
          return new Intl.NumberFormat('en-US', {
            notation: 'compact',
            compactDisplay: 'short'
          }).format(value);
        }
      }
    }
  }
};

// Chart instances storage
const chartInstances = {};

// Time range configurations
const timeRanges = {
  '1D': 1,
  '1W': 7,
  '1M': 30,
  '3M': 90,
  '6M': 180,
  '1Y': 365,
  'ALL': 730
};

// Create a chart
function createChart(containerId, config) {
  const container = document.getElementById(containerId);
  if (!container) return null;
  
  // Create canvas if not exists
  let canvas = container.querySelector('canvas');
  if (!canvas) {
    canvas = document.createElement('canvas');
    container.appendChild(canvas);
  }
  
  const ctx = canvas.getContext('2d');
  
  // Determine color based on trend
  const data = config.data;
  const firstValue = data[0]?.y || 0;
  const lastValue = data[data.length - 1]?.y || 0;
  const isPositive = lastValue >= firstValue;
  
  const lineColor = isPositive ? '#22c55e' : '#ef4444';
  const gradientFill = ctx.createLinearGradient(0, 0, 0, 300);
  gradientFill.addColorStop(0, isPositive ? 'rgba(34, 197, 94, 0.3)' : 'rgba(239, 68, 68, 0.3)');
  gradientFill.addColorStop(1, 'rgba(15, 23, 42, 0)');
  
  const chartConfig = {
    type: 'line',
    data: {
      datasets: [{
        label: config.label || 'Value',
        data: data,
        borderColor: lineColor,
        backgroundColor: gradientFill,
        borderWidth: 2,
        fill: true,
        tension: 0.4,
        pointRadius: 0,
        pointHoverRadius: 5,
        pointHoverBackgroundColor: lineColor,
        pointHoverBorderColor: '#fff',
        pointHoverBorderWidth: 2
      }]
    },
    options: {
      ...chartDefaults,
      plugins: {
        ...chartDefaults.plugins,
        title: {
          display: true,
          text: config.title || '',
          color: '#f1f5f9',
          font: {
            size: 14,
            weight: '600'
          },
          padding: {
            top: 10,
            bottom: 10
          }
        }
      }
    }
  };
  
  // Destroy existing chart if any
  if (chartInstances[containerId]) {
    chartInstances[containerId].destroy();
  }
  
  // Create new chart
  chartInstances[containerId] = new Chart(ctx, chartConfig);
  
  return chartInstances[containerId];
}

// Update chart with new time range
function updateChartTimeRange(containerId, range, baseConfig) {
  const days = timeRanges[range] || 30;
  const newData = generateMockData(days, baseConfig.baseValue, baseConfig.volatility);
  
  createChart(containerId, {
    ...baseConfig,
    data: newData
  });
  
  // Update active button
  const container = document.getElementById(containerId);
  if (container) {
    const timeSelector = container.closest('.chart-wrapper')?.querySelector('.time-selector');
    if (timeSelector) {
      timeSelector.querySelectorAll('button').forEach(btn => {
        btn.classList.toggle('active', btn.textContent === range);
      });
    }
  }
}

// Chart configurations for different assets
const chartConfigs = {
  // Macro charts
  'chart-dxy': {
    title: 'US Dollar Index (DXY)',
    label: 'DXY',
    baseValue: 103.5,
    volatility: 0.015
  },
  'chart-eurusd': {
    title: 'EUR/USD',
    label: 'EUR/USD',
    baseValue: 1.09,
    volatility: 0.012
  },
  'chart-usdjpy': {
    title: 'USD/JPY',
    label: 'USD/JPY',
    baseValue: 148.5,
    volatility: 0.018
  },
  'chart-vix': {
    title: 'VIX Volatility Index',
    label: 'VIX',
    baseValue: 15.2,
    volatility: 0.08
  },
  
  // Gold
  'chart-gold': {
    title: 'Gold Spot (XAU/USD)',
    label: 'Gold',
    baseValue: 2050,
    volatility: 0.015
  },
  
  // Equities
  'chart-ndx': {
    title: 'Nasdaq 100 Index',
    label: 'NDX',
    baseValue: 16500,
    volatility: 0.012
  },
  
  // Crypto
  'chart-btc': {
    title: 'Bitcoin (BTC/USD)',
    label: 'Bitcoin',
    baseValue: 43000,
    volatility: 0.03
  },
  'chart-eth': {
    title: 'Ethereum (ETH/USD)',
    label: 'Ethereum',
    baseValue: 2250,
    volatility: 0.035
  },
  'chart-crypto-total': {
    title: 'Total Crypto Market Cap',
    label: 'Total Market Cap',
    baseValue: 1.65e12,
    volatility: 0.025
  },
  
  // Fixed Income
  'chart-us10y': {
    title: 'US 10-Year Treasury Yield',
    label: '10Y Yield',
    baseValue: 4.15,
    volatility: 0.015
  },
  'chart-us2y': {
    title: 'US 2-Year Treasury Yield',
    label: '2Y Yield',
    baseValue: 4.45,
    volatility: 0.02
  },
  'chart-inflation': {
    title: 'Inflation Expectations',
    label: 'Inflation',
    baseValue: 2.35,
    volatility: 0.01
  },
  'chart-tlt': {
    title: 'TLT - 20+ Year Treasury Bond ETF',
    label: 'TLT',
    baseValue: 93.5,
    volatility: 0.012
  },
  
  // Thematic
  'chart-smh': {
    title: 'SMH - Semiconductor ETF',
    label: 'SMH',
    baseValue: 165,
    volatility: 0.02
  },
  'chart-nvda': {
    title: 'NVIDIA Corporation',
    label: 'NVDA',
    baseValue: 495,
    volatility: 0.025
  },
  'chart-ura': {
    title: 'URA - Uranium ETF',
    label: 'URA',
    baseValue: 28.5,
    volatility: 0.03
  },
  'chart-clean': {
    title: 'ICLN - Clean Energy ETF',
    label: 'ICLN',
    baseValue: 21.8,
    volatility: 0.025
  },
  
  // Growth
  'chart-growth-ndx': {
    title: 'Nasdaq 100 Index',
    label: 'NDX',
    baseValue: 16500,
    volatility: 0.012
  },
  'chart-aapl': {
    title: 'Apple Inc.',
    label: 'AAPL',
    baseValue: 185,
    volatility: 0.015
  },
  'chart-googl': {
    title: 'Alphabet Inc.',
    label: 'GOOGL',
    baseValue: 141,
    volatility: 0.018
  },
  'chart-msft': {
    title: 'Microsoft Corporation',
    label: 'MSFT',
    baseValue: 375,
    volatility: 0.015
  },
  
  // High Beta
  'chart-mstr': {
    title: 'MicroStrategy Inc.',
    label: 'MSTR',
    baseValue: 485,
    volatility: 0.05
  },
  'chart-pltr': {
    title: 'Palantir Technologies',
    label: 'PLTR',
    baseValue: 18.5,
    volatility: 0.045
  },
  'chart-coin': {
    title: 'Coinbase Global',
    label: 'COIN',
    baseValue: 145,
    volatility: 0.04
  },
  'chart-highbeta-nvda': {
    title: 'NVIDIA Corporation',
    label: 'NVDA',
    baseValue: 495,
    volatility: 0.025
  }
};

// Initialize all charts on page load
function initializeCharts() {
  Object.keys(chartConfigs).forEach(chartId => {
    const config = chartConfigs[chartId];
    const data = generateMockData(90, config.baseValue, config.volatility); // Default 3M
    
    createChart(chartId, {
      ...config,
      data: data
    });
  });
}

// Initialize when DOM is ready
if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeCharts);
} else {
  initializeCharts();
}

// Export for global use
window.FinSightCharts = {
  createChart,
  updateChartTimeRange,
  chartConfigs,
  timeRanges
};

