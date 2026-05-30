// DOM ready handler
document.addEventListener("DOMContentLoaded", function () {
  console.log("DOM loaded");
  console.log("All tab contents:", document.querySelectorAll('.tab-content'));

  // Always show the invoices tab by default
  showTab('invoices');

  // Setup search functionality
  setupSearch();

  // Apply fixed column structure to tables
  // initFixedColumns(); // Example placeholder for future use
});

function showTab(tabId) {
  // Hide all tab contents
  document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));

  // Show selected tab content
  const selectedTab = document.getElementById(tabId);
  if (selectedTab) {
    selectedTab.classList.remove('hidden');
  }

  // Remove active class from all buttons
  document.querySelectorAll('.tab-button').forEach(btn => {
    btn.classList.remove('active');
  });

  // Add active class to clicked button
  const activeButton = document.querySelector(`[onclick="showTab('${tabId}')"]`);
  if (activeButton) {
    activeButton.classList.add('active');
  }

  // Optional: Re-initialize table search/filtering
  // setupSearch();
}


// Setup search input event listeners
function setupSearch() {
  // Remove previous event listeners if any exist
  removeSearchListeners();

  // Get all possible search inputs across tabs
  const pInvoiceSearch = document.getElementById("p_searchInput");
  const bInvoiceSearch = document.getElementById("b_searchInput");
  const pCNSearch = document.getElementById("cn_p_searchInput");
  const bCNSearch = document.getElementById("cn_b_searchInput");
  const pDNSearch = document.getElementById("dn_p_searchInput");
  const bDNSearch = document.getElementById("dn_b_searchInput");

  // Store references to avoid duplication
  window.pInvoiceSearch = pInvoiceSearch;
  window.bInvoiceSearch = bInvoiceSearch;
  window.pCNSearch = pCNSearch;
  window.bCNSearch = bCNSearch;
  window.pDNSearch = pDNSearch;
  window.bDNSearch = bDNSearch;

  // Add new event listeners
  if (pInvoiceSearch) {
    pInvoiceSearch.addEventListener("input", function () {
      const filter = this.value;
      const tableId = "p_invoiceTable";
      filterTable(tableId, filter);
    });
  }

  if (bInvoiceSearch) {
    bInvoiceSearch.addEventListener("input", function () {
      const filter = this.value;
      const tableId = "b_invoiceTable";
      filterTable(tableId, filter);
    });
  }

  if (pCNSearch) {
    pCNSearch.addEventListener("input", function () {
      const filter = this.value;
      const tableId = "p_cnTable";
      filterTable(tableId, filter);
    });
  }

  if (bCNSearch) {
    bCNSearch.addEventListener("input", function () {
      const filter = this.value;
      const tableId = "b_cnTable";
      filterTable(tableId, filter);
    });
  }

  if (pDNSearch) {
    pDNSearch.addEventListener("input", function () {
      const filter = this.value;
      const tableId = "p_dnTable";
      filterTable(tableId, filter);
    });
  }

  if (bDNSearch) {
    bDNSearch.addEventListener("input", function () {
      const filter = this.value;
      const tableId = "b_dnTable";
      filterTable(tableId, filter);
    });
  }
}

// Remove existing event listeners before re-adding
function removeSearchListeners() {
  if (window.pInvoiceSearch) {
    const oldInput = window.pInvoiceSearch;
    const newInput = oldInput.cloneNode(true);
    oldInput.replaceWith(newInput);
    window.pInvoiceSearch = newInput;
  }

  if (window.bInvoiceSearch) {
    const oldInput = window.bInvoiceSearch;
    const newInput = oldInput.cloneNode(true);
    oldInput.replaceWith(newInput);
    window.bInvoiceSearch = newInput;
  }

  if (window.pCNSearch) {
    const oldInput = window.pCNSearch;
    const newInput = oldInput.cloneNode(true);
    oldInput.replaceWith(newInput);
    window.pCNSearch = newInput;
  }

  if (window.bCNSearch) {
    const oldInput = window.bCNSearch;
    const newInput = oldInput.cloneNode(true);
    oldInput.replaceWith(newInput);
    window.bCNSearch = newInput;
  }

  if (window.pDNSearch) {
    const oldInput = window.pDNSearch;
    const newInput = oldInput.cloneNode(true);
    oldInput.replaceWith(newInput);
    window.pDNSearch = newInput;
  }

  if (window.bDNSearch) {
    const oldInput = window.bDNSearch;
    const newInput = oldInput.cloneNode(true);
    oldInput.replaceWith(newInput);
    window.bDNSearch = newInput;
  }
}

// Set up fixed columns


// Filter table by search input
function filterTable(tableId, filter) {
  const table = document.getElementById(tableId);
  if (!table) {
    console.warn(`Table ${tableId} not found!`);
    return;
  }

  const rows = table.querySelectorAll("tbody tr");
  filter = filter.toLowerCase();

  const isDateSearch = /^\d{1,4}[-./]\d{1,2}[-./]\d{1,4}$/.test(filter) ||
                       /^\d{1,2}$/.test(filter) || /^\d{4}$/.test(filter);

  rows.forEach(row => {
    const cells = row.getElementsByTagName("td");
    let match = false;

    for (let i = 0; i < cells.length; i++) {
      const cellText = cells[i]?.textContent.toLowerCase().trim() || "";
      if (isDateSearch && i === 3) {
        if (
          /^\d{4}$/.test(filter) && cellText.includes(filter) ||
          (/^\d{1,2}$/.test(filter) &&
            (cellText.split("-")[1] === filter.padStart(2, "0") ||
             cellText.split("-")[2] === filter.padStart(2, "0")))
        ) {
          match = true;
          break;
        } else if (cellText.includes(filter)) {
          match = true;
          break;
        }
      } else if (cellText.includes(filter)) {
        match = true;
        break;
      }
    }

    row.style.display = match ? "" : "none";
  });
}

// Sort table by column
function sortTable(tableId, columnIndex) {
  const table = document.getElementById(tableId);
  if (!table) return;

  const tbody = table.querySelector("tbody");
  if (!tbody) return;

  const headers = table.querySelectorAll("th");
  headers.forEach(th => th.classList.remove("sorted-asc", "sorted-desc"));

  const currentHeader = headers[columnIndex];
  const currentSortColumn = table.getAttribute("data-sort-column");
  let currentSortDir = table.getAttribute("data-sort-dir") || "asc";

  if (currentSortColumn == columnIndex) {
    currentSortDir = currentSortDir === "asc" ? "desc" : "asc";
  } else {
    currentSortDir = "asc";
  }

  table.setAttribute("data-sort-dir", currentSortDir);
  table.setAttribute("data-sort-column", columnIndex);
  currentHeader.classList.add(currentSortDir === "asc" ? "sorted-asc" : "sorted-desc");

  const rows = Array.from(tbody.querySelectorAll("tr"));

  rows.sort((a, b) => {
    const cellA = a.children[columnIndex]?.textContent.trim() || "";
    const cellB = b.children[columnIndex]?.textContent.trim() || "";
    let result;

    if (columnIndex === 3) {
      const dateA = parseDate(cellA);
      const dateB = parseDate(cellB);
      result = dateA && dateB ? dateA - dateB : cellA.localeCompare(cellB);
    } else if (isNumericColumn(columnIndex)) {
      const numA = parseFloat(cellA.replace(/[₹,]/g, ""));
      const numB = parseFloat(cellB.replace(/[₹,]/g, ""));
      result = !isNaN(numA) && !isNaN(numB) ? numA - numB : cellA.localeCompare(cellB);
    } else {
      result = cellA.localeCompare(cellB);
    }

    return currentSortDir === "desc" ? -result : result;
  });

  while (tbody.firstChild) tbody.removeChild(tbody.firstChild);
  rows.forEach(row => tbody.appendChild(row));
}

// Parse date strings
function parseDate(dateStr) {
  if (/^\d{4}-\d{2}-\d{2}$/.test(dateStr)) return new Date(dateStr);

  const formats = [
    str => new Date(str),
    str => {
      const [day, month, year] = str.split(/[-./]/);
      return new Date(`${year}-${month}-${day}`);
    },
    str => {
      const [month, day, year] = str.split(/[-./]/);
      return new Date(`${year}-${month}-${day}`);
    },
  ];

  for (const formatFn of formats) {
    const date = formatFn(dateStr);
    if (!isNaN(date.getTime())) return date;
  }

  return null;
}

// Identify numeric columns
function isNumericColumn(columnIndex) {
  return columnIndex >= 4 && columnIndex <= 6;
}



function getActiveTabId() {
  const tabs = document.querySelectorAll(".tab-content");
  for (let tab of tabs) {
    if (!tab.classList.contains("hidden")) {
      return tab.id;
    }
  }
  return "invoices";
}

function getAllSearchQueries() {
  const searchInputs = {
    invoices: ["p_searchInput", "b_searchInput"],
    credit_notes: ["cn_p_searchInput", "cn_b_searchInput"],
    debit_notes: ["dn_p_searchInput", "dn_b_searchInput"]
  };

  let allQueries = [];

  for (const tabId in searchInputs) {
    const ids = searchInputs[tabId];
    for (let id of ids) {
      const input = document.getElementById(id);
      if (input && input.value.trim()) {
        allQueries.push(input.value.trim());
      }
    }
  }

  // Return combined unique search terms
  return [...new Set(allQueries)];
}

function shareFilteredData() {
  const active_tab = getActiveTabId();
  const allQueries = getAllSearchQueries(); // Get all search values
  const gstin = document.getElementById("current-gstin").value;

  const baseUrl = "/public-table/";
  const params = new URLSearchParams();

  if (gstin) params.set("gstin", gstin);


  // If multiple queries exist, join them with a space or use first
  const query = allQueries.join(' '); // You can also do allQueries[0] if only one needed
  if (query) params.set("q", query);

  params.set("tab", active_tab);

  const fullUrl = window.location.origin + baseUrl + "?" + params.toString();
  const whatsappMessage = encodeURIComponent(`Check out this filtered GST data:\n\n${fullUrl}`);
  const whatsappUrl = `https://wa.me/?text= ${whatsappMessage}`;
  window.open(whatsappUrl, "_blank");
}


const scrollButton = document.getElementById('scrollButton');
let isAtTop = true;

scrollButton.addEventListener('click', () => {
    if (isAtTop) {
        window.scrollTo({
            top: document.body.scrollHeight,
            behavior: 'smooth'
        });
        scrollButton.textContent = '↑';
        scrollButton.title = 'Scroll to Top';
    } else {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
        scrollButton.textContent = '↓';
        scrollButton.title = 'Scroll to Bottom';
    }
    isAtTop = !isAtTop;
});

  // Update button state based on scroll position
  window.addEventListener('scroll', () => {
      const scrollPosition = window.scrollY;
      const windowHeight = window.innerHeight;
      const documentHeight = document.body.scrollHeight;

      if (scrollPosition + windowHeight >= documentHeight - 10) {
          isAtTop = false;
          scrollButton.textContent = '↑';
          scrollButton.title = 'Scroll to Top';
      } else if (scrollPosition <= 10) {
          isAtTop = true;
          scrollButton.textContent = '↓';
          scrollButton.title = 'Scroll to Bottom';
      }
  });


