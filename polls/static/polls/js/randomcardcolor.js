var cards = $('.card');
var classes = ['card-color-1', 'card-color-2', 'card-color-3', 'card-color-4', 'card-color-5', 'card-color-6'];

function randomAddClass(cards, classes) {
    // shuffle classes here
    for (var i = 0; i < cards.length; i++) {
        var dclass = classes[i % classes.length];
        console.log(cards[i]);
        console.log(classes[i]);
        $(cards[i]).addClass(dclass);
    }
}

randomAddClass(cards, classes);