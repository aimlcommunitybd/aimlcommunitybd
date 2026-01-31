document.addEventListener('DOMContentLoaded', function() {
    const portfolioContainer = document.querySelector('.isotope-container');
    const portfolioFilters = document.querySelectorAll('.isotope-filters li');
    const loadMoreBtn = document.getElementById('load-more-btn');
    const loadMoreContainer = document.getElementById('load-more-container');
    let maxItemsForAll = 6; // Initial limit
    const incrementBy = 6; // Load 9 more each time
    
    if (portfolioContainer) {
        const allItems = portfolioContainer.querySelectorAll('.isotope-item');
        const totalItems = allItems.length;
        
        allItems.forEach((item, index) => {
            item.setAttribute('data-index', index + 1);
        });

        const isotope = new Isotope(portfolioContainer, {
            itemSelector: '.isotope-item',
            layoutMode: 'masonry',
            getSortData: {
                originalOrder: function(itemElem) {
                    return itemElem.getAttribute('data-original-order') || 0;
                }
            }
        });

        function filterItems(filterValue) {
            if (filterValue === '*') {
                isotope.arrange({
                    filter: function(itemElem) {
                        const index = parseInt(itemElem.getAttribute('data-index'));
                        return index <= maxItemsForAll;
                    }
                });
                
                // Show/hide load more button
                if (maxItemsForAll < totalItems) {
                    loadMoreContainer.style.display = 'block';
                } else {
                    loadMoreContainer.style.display = 'none';
                }
            } else {
                isotope.arrange({
                    filter: filterValue
                });
                loadMoreContainer.style.display = 'none';
            }
        }

        // Initial filter
        filterItems('*');

        // Filter on button click
        portfolioFilters.forEach(function(filter) {
            filter.addEventListener('click', function() {
                portfolioFilters.forEach(f => f.classList.remove('filter-active'));
                this.classList.add('filter-active');
                
                const filterValue = this.getAttribute('data-filter');
                
                // Reset max items when switching filters
                maxItemsForAll = 9;
                
                filterItems(filterValue);
            });
        });

        // Load more functionality
        if (loadMoreBtn) {
            loadMoreBtn.addEventListener('click', function() {
                maxItemsForAll += incrementBy;
                filterItems('*');
                
                // Smooth scroll to newly loaded items
                setTimeout(() => {
                    const firstNewItem = portfolioContainer.querySelector(`[data-index="${maxItemsForAll - incrementBy + 1}"]`);
                    if (firstNewItem) {
                        firstNewItem.scrollIntoView({ behavior: 'smooth', block: 'center' });
                    }
                }, 300);
            });
        }

        portfolioContainer.addEventListener('load', function() {
            isotope.layout();
        }, true);
    }
});