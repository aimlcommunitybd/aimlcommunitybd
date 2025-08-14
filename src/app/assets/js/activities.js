// 1. First, include Isotope.js in your HTML head section or before closing body tag:
// <script src="https://unpkg.com/isotope-layout@3/dist/isotope.pkgd.min.js"></script>

// 2. Add this JavaScript code after the DOM is loaded:
document.addEventListener('DOMContentLoaded', function() {
    // Initialize Isotope
    const portfolioContainer = document.querySelector('.isotope-container');
    const portfolioFilters = document.querySelectorAll('.isotope-filters li');
    
    if (portfolioContainer) {
        // Initialize Isotope
        const isotope = new Isotope(portfolioContainer, {
            itemSelector: '.isotope-item',
            layoutMode: 'masonry',
            getSortData: {
                originalOrder: function(itemElem) {
                    return itemElem.getAttribute('data-original-order') || 0;
                }
            }
        });

        // Filter items on button click
        portfolioFilters.forEach(function(filter) {
            filter.addEventListener('click', function() {
                // Remove active class from all filters
                portfolioFilters.forEach(f => f.classList.remove('filter-active'));
                
                // Add active class to clicked filter
                this.classList.add('filter-active');
                
                // Get filter value
                const filterValue = this.getAttribute('data-filter');
                
                // Filter items
                isotope.arrange({
                    filter: filterValue === '*' ? '*' : filterValue
                });
            });
        });

        // Layout after images load (optional but recommended)
        portfolioContainer.addEventListener('load', function() {
            isotope.layout();
        }, true);
    }
});

// Alternative implementation if you prefer jQuery (requires jQuery):
/*
$(document).ready(function() {
    // Initialize Isotope
    var $grid = $('.isotope-container').isotope({
        itemSelector: '.isotope-item',
        layoutMode: 'masonry'
    });

    // Filter items on button click
    $('.isotope-filters li').on('click', function() {
        $('.isotope-filters li').removeClass('filter-active');
        $(this).addClass('filter-active');
        
        var filterValue = $(this).attr('data-filter');
        $grid.isotope({ filter: filterValue });
    });
});
*/