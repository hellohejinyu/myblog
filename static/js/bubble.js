(function () {
    var width, height, canvas, ctx, circles;
    function initHeader() {
        try {
            canvas = document.getElementById('bubbleCanvas');
            if(canvas){
                //width = window.innerWidth*0.25>300?window.innerWidth*0.25:300;
                //height = window.innerHeight;
                width = 300;
                height = 130;

                canvas.width = width;
                canvas.height = height;
                ctx = canvas.getContext('2d');
                circles = [];
                for (var x = 0; x < width * 0.5; x++) {
                    var c = new Circle();
                    circles.push(c);
                }
                animate();
            }
        } catch (ex) {
            if (window.cosole && window.cosole.log) {
                cosole.log(ex)
            }
        }
    }

    function animate() {
        ctx.clearRect(0, 0, width, height);
        for (var i in circles) {
            circles[i].draw();
        }
        window.requestAFrame = (function () {
            return window.requestAnimationFrame || window.webkitRequestAnimationFrame || window.mozRequestAnimationFrame || window.oRequestAnimationFrame || window.msRequestAnimationFrame ||
                    function (callback) {
                        return window.setTimeout(callback, 1000 / 60); // shoot for 60 fps
                    };
        })();
        requestAFrame(animate);
    }

// Canvas manipulation
    function Circle() {
        var _this = this;

        // constructor
        (function () {
            _this.pos = {};
            init();
        })();

        function init() {
            _this.pos.x = Math.random() * width;
            _this.pos.y = height + Math.random() * 100;
            _this.alpha = 0.5 + Math.random() * 0.3;
            _this.scale = 0.1 + Math.random() * 0.3;
            _this.velocity = Math.random();
        }

        this.draw = function () {
            if (_this.alpha <= 0) {
                init();
            }
            _this.pos.y -= _this.velocity;
            _this.alpha -= 0.001;
            ctx.beginPath();
            ctx.arc(_this.pos.x, _this.pos.y, _this.scale * 10, 0, 2 * Math.PI, false);
            ctx.fillStyle = 'rgba(255,255,255,' + _this.alpha + ')';
            ctx.fill();
        };
    }

    initHeader();
}());