/** Hotel Arena — hero slide show.
 *
 *  Crossfades the hero backgrounds and drives the dot navigation. Kept
 *  deliberately small: no Odoo widget registration, so it also runs on
 *  editor-created pages that carry the snippet.
 */
(function () {
    "use strict";

    var INTERVAL = 6000;

    function initSlider(root) {
        var slides = root.querySelectorAll(".ha-hero-slide");
        var dots = root.querySelectorAll(".ha-hero-dot");
        if (slides.length < 2) {
            return;
        }

        var current = 0;
        var timer = null;

        function show(index) {
            current = (index + slides.length) % slides.length;
            for (var i = 0; i < slides.length; i++) {
                slides[i].classList.toggle("is-active", i === current);
            }
            for (var d = 0; d < dots.length; d++) {
                dots[d].classList.toggle("is-active", d === current);
                dots[d].setAttribute("aria-selected", d === current ? "true" : "false");
            }
        }

        function start() {
            stop();
            timer = window.setInterval(function () {
                show(current + 1);
            }, INTERVAL);
        }

        function stop() {
            if (timer) {
                window.clearInterval(timer);
                timer = null;
            }
        }

        for (var n = 0; n < dots.length; n++) {
            (function (index) {
                dots[index].addEventListener("click", function () {
                    show(index);
                    start();
                });
            })(n);
        }

        // Pausing while the tab is hidden keeps the Ken Burns zoom in sync
        // with what the visitor actually sees.
        document.addEventListener("visibilitychange", function () {
            if (document.hidden) {
                stop();
            } else {
                start();
            }
        });

        show(0);
        start();
    }

    function init() {
        var roots = document.querySelectorAll(".s_ha_hero_slider");
        for (var i = 0; i < roots.length; i++) {
            initSlider(roots[i]);
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
