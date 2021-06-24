var Sortable = function(element){
    var rect;
    var self = this;
    this.element = element;
    this.items = this.element.querySelectorAll(this.element.dataset.sortable);
    rect = this.items[0].getBoundingClientRect();
    this.item_width = Math.floor(rect.width);
    this.item_heigth = Math.floor(rect.height);
    this.cols = Math.floor(this.element.offsetWidth / this.item_width);
    this.element.style.height = (this.item_heigth * Math.ceil(this.items.length / this.cols)) + "px";

    for(var i = 0; i < this.items.length; i++) {
        var item = this.items[i];
        item.style.position = "absolute";
        item.style.top = "0px";
        item.style.left = "0px";
        var position = item.dataset.position;
        this.moveItem(item, item.dataset.position)
    }
    interact(this.element.dataset.sortable, {
        context: this.element
    }).draggable({
        inertia: false,
        manualStart: false,
        onmove: function(e){
            self.move(e)
        }
    }).on('dragstart', function(e){
        var r = e.target.getBoundingClientRect();
        e.target.classList.add('is-dragged');
        self.startPosition = e.target.dataset.position;
        self.offset = {
            x: e.clientX - r.left,
            y: e.clientY - r.top
        }
    }).on('dragend', function(e){
        e.target.classList.remove('is-dragged');
        self.moveItem(e.target, e.target.dataset.position);
    })
};

Sortable.prototype.move = function(e){
    var p = this.getXY(this.startPosition);
    var x = p.x + e.clientX - e.clientX0;
    var y = p.y + e.clientY - e.clientY0;
    e.target.style.transform = "translate3D(" + x + "px, " + y + "px, 0)";
    var oldPosition = e.target.dataset.position;
    var newPosition = this.guessPosition(x + this.offset.x, y + this.offset.y)
    if(oldPosition != newPosition){
        this.swap(oldPosition, newPosition);
        e.target.dataset.position = newPosition
    }
    this.guessPosition(x, y);
};

Sortable.prototype.getXY = function(position){
    var x = this.item_width * (position % this.cols);
    var y = this.item_heigth * Math.floor(position / this.cols);
    return {
        x: x,
        y: y
    }
};

Sortable.prototype.guessPosition = function(x, y){
    var col = Math.floor(x / this.item_width)
    if(col >= this.cols){
        col = this.cols -1;
    }
    if(col <= 0){
        col = 0;
    }
    var row = Math.floor(y / this.item_heigth)
    if(row < 0){
        row = 0;
    }
    var position = col + row * this.cols;
    if(position >= this.items/length){
        return this.items.length - 1;
    }
    return position
};

Sortable.prototype.swap = function(start, end){
    for(var i = 0; i < this.items.length; i++) {
        var item = this.items[i];
        if(!item.classList.contains('is-dragged')){
            var position = parseInt(item.dataset.position, 10);
            if(position >= end && position < start && end < start){
                this.moveItem(item, position +1);
            }else if(position <= end && position > start && end > start){
                this.moveItem(item, position -1);
            }
        }
    }
};

Sortable.prototype.moveItem = function(item, position){
    var p = this.getXY(position);
    item.style.transform = "translate3D(" + p.x + "px, " + p.y + "px, 0)";
    item.dataset.position = position;
    let formData2 = new FormData();
    formData2.append('storyboard_id', item.dataset.storyboard);
    formData2.append('case_id', item.dataset.id);
    formData2.append('text_order', item.dataset.position);
    var classNameSearched =  '#getText' + item.dataset.text;
    result = $(classNameSearched).text()
    resultLength = result.length -1
    result = result.substring(0,resultLength)
    formData2.append('text', result);
    const request2 = new Request('/update_case_order_storyboard/', {method: 'POST', body: formData2, headers: {'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value}});
    fetch(request2)
        .then(response => response.json())
        .then(result => {})
};