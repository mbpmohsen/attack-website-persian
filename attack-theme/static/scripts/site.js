// position body according to header size
function positionBody() {
    var headerHeight = $(".navbar").outerHeight();
    var viewportHeight = $(".attack-website-wrapper").outerHeight();
    $(".sidebar.nav").css({
        "top": headerHeight + "px",
        "max-height": viewportHeight - headerHeight + "px"
    });
}

//scroll the active element into view in the sidenav
function initSidenavScroll() {
    var sidenav = $(".sidenav-list");
    var sidenav_active_elements = $(".sidenav .active");
    if (sidenav_active_elements.length > 0) {
        setTimeout(function() { //setTimeout gives bootstrap time to execute first
            sidenav[0].scrollTop = sidenav_active_elements[0].offsetTop - 60;
        });
    }
}

// when the document loads, position the body
$(document).ready(function() {
    positionBody();
    initSidenavScroll();
    $('[data-toggle="tooltip"]').tooltip();
});

// when the document resizes, position body
$(window).resize(function() {
    positionBody();;
});
