$(document).ready(function () {
  const
    markBtn = $('.mark-btn'),
    followBtn = $('.follow-btn');

  $(markBtn).on('click', function() {
    const icon = $(this).children('i');
    const post_id = $(this).attr('data-post-id');
    let url, _html;
    if( $(icon).html() === 'bookmark_border') {
      url = `/post/${post_id}/mark-read`
      _html = 'bookmark'
    } else {
      url = `/post/${post_id}/mark-unread`
      _html = 'bookmark_border'
    }
    $.post(url, function() {
      $(icon).html(_html);
    });
  });

  const FOLLOWED = 'followed';
  const UNFOLLOWED = 'unfollowed';

  $(followBtn).on('click', function() {
    const state = $(this).hasClass(FOLLOWED) ? FOLLOWED : UNFOLLOWED;
    const username = $(this).attr('data-username');
    // console.log(state, username, $(this));

    let url, class_remove, class_add;

    if(state === UNFOLLOWED) {
      url = `/profile/${username}/follow`;
      class_remove = UNFOLLOWED;
      class_add = FOLLOWED;
      html = 'Following';
    } else {
      url = `/profile/${username}/unfollow`;
      class_remove = FOLLOWED;
      class_add = UNFOLLOWED;
      html = 'Follow';
    }


    $.post(url, () => {
      $(this).removeClass(class_remove);
      $(this).addClass(class_add);
      $(this).html(html);
    });

  });



  

});