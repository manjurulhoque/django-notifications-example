/**
 * Created by Rumi on 6/12/2017.
 */

// (function worker() {
//     $.ajax({
//         url: 'http://127.0.0.1:8000/notifications/api/all_list/',
//         success: function (res) {
//             console.log(res);
//             // if ($('.unread-noty').text() !== res.unread_count) {
//             //     $('.unread-noty').text(res.unread_count);
//             // }
//         },
//         complete: function () {
//             // Schedule the next request when the current one's complete
//             // setTimeout(worker, 5000);
//         }
//     });
// })();

notify_menu_class = "drop-content";

function my_special_notification_callback(data) {
    let menus = document.getElementsByClassName(notify_menu_class);
    if (menus) {
        let messages = data.unread_list.map(function (item) {
            let message = "";
            let unread = '';
            let username = '';
            let verb = '';
            let timestamp = '';
            // if (typeof item.actor !== 'undefined') {
            //     message = item.actor;
            // }
            // if (typeof item.verb !== 'undefined') {
            //     message = message + " " + item.verb;
            // }
            // if (typeof item.target !== 'undefined') {
            //     message = message + " " + item.target;
            // }
            // if (typeof item.timestamp !== 'undefined') {
            //     message = message + " " + item.timestamp;
            // }
            if (typeof item.unread !== 'undefined' && item.unread === true) {
                unread = 'alert alert-light';
            }
            if (typeof item.actor !== 'undefined') {
                username = item.actor;
            }
            if (typeof item.verb !== 'undefined') {
                verb = item.verb;
            }
            if (typeof item.timestamp !== 'undefined') {
                timestamp = item.timestamp;
            }
            return '<li class="row ' + unread + '">\n' +
                '                                    <div class="col-md-3 col-sm-3 col-xs-3">\n' +
                '                                        <div class="notify-img">\n' +
                '                                            <img src="http://placehold.it/45x45" alt="">\n' +
                '                                        </div>\n' +
                '                                    </div>\n' +
                '                                    <div class="col-md-9 col-sm-9 col-xs-9 pd-l0">\n' +
                '                                        <p>' + username + ' ' + verb + '</p>\n' +
                '                                        <a href="" class="rIcon"><i class="fa fa-dot-circle-o"></i></a>\n' +
                '                                        <p class="time">' + timestamp + ' ago</p>\n' +
                '                                    </div>\n' +
                '                                </li>';
            // return '<li class="row ' + unread + '">' + message + '</li>';
        }).join('');

        for (let i = 0; i < menus.length; i++) {
            menus[i].innerHTML = messages;
        }
    }
}

$(document).ready(function () {
    $('.mark-as-read').on('click', function () {

    })
});