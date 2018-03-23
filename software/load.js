    var app = document.querySelector('#app');
    app.baseUrl = '/';

      document.addEventListener('WebComponentsReady', function() {
        var tabs = document.querySelector('paper-tabs');
            var temp= $(window).width();
            if (temp < 700){
            tabs.style.visibility='hidden';
            }
            else{
            tabs.style.visibility='visible';
            };

        tabs.selected="3";
        //app.route="/";
        var menu = document.querySelector('paper-menu');
        //var appr = document.querySelector('app-route');
        //appr.addEventListener('route-changed', function(){
        //    console.log('1234567');
        //});
        var drawer = document.querySelector('paper-drawer-panel');
        menu.addEventListener('iron-activate', function() {
            drawer.closeDrawer();
        });
        window.addEventListener("resize", function(){
            var temp= $(window).width();
            if (temp < 700){
            tabs.style.visibility='hidden';
            }
            else{
            tabs.style.visibility='visible';
            };
            });
        });
