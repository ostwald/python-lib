
function log(s) {
    if (window.console)
        console.log(s);
}

$(function () {

    // Initiallize the tree
    var collapse_threshold_level = 3;
    $('.body').each (function (i, body) {
        var $body = $(body);
        var className = $body.attr('class')
        var level = parseInt(className.replace('body level', ''));
        if (level < collapse_threshold_level) {
            $body.hide()
        }
    })

    $('.branch').mouseover (function (event) {
//        $(event.target).css ('background', 'yellow')
    })

    log ($('.leaf').size() + ' Leaves found');

    $('.branch .label')
        .click (function (event) {
            var $branch = $(event.target).closest('.branch');
            var className = $branch.attr('class')

            // we completely bank on class of form: "branch levelN"
            // and our body has the same levelN class ....
            var level = className.split(' ')[1];

            // first find the branch
            $body = $branch.find ('.body.' + level)
            var visible = $body.is(":visible")
            if (event.shiftKey) {
                if (visible) {
                    $branch.find('.body').hide()
                } else {
                    $branch.find('.body').show()
                }
            } else {
//                $body.toggle()
                if (visible) {
                    $body.slideUp(500)
                } else {
                    $body.slideDown(500)
                }
          }

        });

});