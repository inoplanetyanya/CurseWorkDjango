$(function() {
  
  $('.toggle-categories-btn').click(function(){
    if ($(this).text() === 'Показать категории') {
      $(this).text('Скрыть категории');
      $('.categories').toggleClass('hidden')
    } else {
      $(this).text('Показать категории');
      $('.categories').toggleClass('hidden');
    }
  })

});