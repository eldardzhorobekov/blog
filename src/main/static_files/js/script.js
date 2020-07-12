$(document).ready(function () {
  // Initalize materialize Modal component
  $('.modal').modal();

  const markBtn = $('.mark-btn');
  const followBtn = $('.follow__btn');

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
  const FOLLOWED_HTML = 'Following';
  const UNFOLLOWED = 'unfollowed';
  const UNFOLLOWED_HTML = 'Follow';

  function toggleFollowBtn(btn) {
    // Toggle class and html value of button

    const is_following = $(btn).hasClass(FOLLOWED);
    
    $(btn).removeClass(UNFOLLOWED);
    $(btn).removeClass(FOLLOWED);

    if(is_following) {
      $(btn).addClass(UNFOLLOWED);
      $(btn).html(UNFOLLOWED_HTML);
    } else {
      $(btn).addClass(FOLLOWED);
      $(btn).html(FOLLOWED_HTML);
    }
  }

  $(followBtn).on('click', function() {
    // This function makes AJAX request to server to make subscription
    // and toggles the button's class and html value
    const that = this;
    const is_following = $(this).hasClass(FOLLOWED);
    const username = $(this).attr('data-username');
    const url = `/profile/${username}/` + (is_following ? 'unfollow' : 'follow');
    $
      .post(url, () => {
        // console.log('Sending');
      })
      .done(() => {
        toggleFollowBtn(that);
        // console.log('Success!');
      })
      .fail(() => {
        console.error('No subscription');
      });
  });


  function generateFollowItem(username='username', is_following=true) {
    // This function creates:
    // <li class="follow__item">
    //   <a href="#" class="material-icon__wrapper">
    //     <i class="material-icons">person</i>
    //     <span class="black-text">{{ username }}</span>
    //   </a>
    //   <a href="#" class="follow__btn followed" data-username="{{ username }}">Following</a>
    // </li>

    // Toggles button if is_following == false

    const parent_li = $('<li/>').addClass('follow__item');
    const user_a = $('<a/>').attr('href', '#').addClass('material-icon__wrapper follow__user').appendTo(parent_li);
    const user_icon_i = $('<i/>').addClass('material-icons').html('person').appendTo(user_a);
    const user_name_span = $('<span/>').html(username).addClass('black-text').appendTo(user_a);
    const follow_btn = $('<a/>').attr('href','#').addClass('follow__btn '+FOLLOWED).attr('data-username', username).html(FOLLOWED_HTML).appendTo(parent_li);
    
    if(!is_following) toggleFollowBtn(follow_btn);

    return parent_li;
  }

  const followers_list = $('.follow__followers_list');
  // for testing purpose
  for(let i=0; i < 10; ++i) {
    generateFollowItem(username='Followed user', is_following=true).appendTo(followers_list);
  }
  for(let i=0; i < 5; ++i) {
    generateFollowItem(username='Unfollowed user', is_following=false).appendTo(followers_list);
  }
});