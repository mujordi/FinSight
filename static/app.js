// Tab switching with enhanced UX
function tab(id) {
  // Remove active class from all tabs and buttons
  document.querySelectorAll('.tab').forEach(t => t.classList.remove('active'));
  document.querySelectorAll('nav button').forEach(b => b.classList.remove('active'));
  
  // Add active class to selected tab
  const selectedTab = document.getElementById(id);
  if (selectedTab) {
    selectedTab.classList.add('active');
  }
  
  // Add active class to corresponding button
  const activeButton = event?.target;
  if (activeButton && activeButton.tagName === 'BUTTON') {
    activeButton.classList.add('active');
  }
  
  // Save current tab to localStorage for persistence
  localStorage.setItem('activeTab', id);
  
  // Scroll to top smoothly
  window.scrollTo({ top: 0, behavior: 'smooth' });
}

// Initialize: restore last active tab or default to first
document.addEventListener('DOMContentLoaded', () => {
  const savedTab = localStorage.getItem('activeTab') || 'macro';
  const tabElement = document.getElementById(savedTab);
  
  if (tabElement) {
    tabElement.classList.add('active');
    
    // Find and activate corresponding button
    const buttons = document.querySelectorAll('nav button');
    buttons.forEach(btn => {
      if (btn.getAttribute('onclick')?.includes(savedTab)) {
        btn.classList.add('active');
      }
    });
  }
  
  // Add keyboard navigation
  document.addEventListener('keydown', (e) => {
    if (e.key === 'ArrowLeft' || e.key === 'ArrowRight') {
      const buttons = Array.from(document.querySelectorAll('nav button'));
      const activeButton = buttons.find(b => b.classList.contains('active'));
      const currentIndex = buttons.indexOf(activeButton);
      
      let nextIndex;
      if (e.key === 'ArrowLeft') {
        nextIndex = currentIndex > 0 ? currentIndex - 1 : buttons.length - 1;
      } else {
        nextIndex = currentIndex < buttons.length - 1 ? currentIndex + 1 : 0;
      }
      
      buttons[nextIndex]?.click();
    }
  });
  
  // Add loading indicators for iframes
  const iframes = document.querySelectorAll('.chart iframe');
  iframes.forEach(iframe => {
    iframe.addEventListener('load', () => {
      iframe.parentElement.classList.add('loaded');
    });
  });
  
  // Add smooth hover effects for table rows
  const rows = document.querySelectorAll('tbody tr');
  rows.forEach(row => {
    row.addEventListener('mouseenter', () => {
      row.style.transform = 'scale(1.01)';
    });
    row.addEventListener('mouseleave', () => {
      row.style.transform = 'scale(1)';
    });
  });
});
