function updateBooklist( booklist )
{
  $('#quiz').remove();

  if( $('#book_table').length == 0){
    var $table = $('<table/>');
    $table.attr('id', 'book_table');
    $('#bottom').append($table);
  } 
  
  $('#book_table').children().remove();
  
  for(var i=0; i<booklist.length; i++) {
    book = booklist[i]
    $('#book_table').append( '<tr id=' + book.question_id + '><td id=' + book.id + '>' + book.title + '</td><td>' + book.author + '</td></tr>' );
  };
  book_table_click();
  new $.sygTrHighlighter('table#book_table');
};


var val_book_hint = "";

function refrect_hint(){
  new_val_book_hint = $("#book_hint").val();
  if(val_book_hint == new_val_book_hint){
    return
  }
  val_book_hint = new_val_book_hint
  
  $.ajax({
    url: "./books_info",
    type: "POST",
    data: { val_book_hint: val_book_hint},
    dataType: 'json',
    success: function(arr) {
      var booklist = JSON.parse(arr);
      updateBooklist (booklist)
    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
      alert(textStatus);
    }
  });
}

function book_table_click(){
  $('#book_table tr').click( begin_question );
}

function show_amazon_info(title, author){
  $.ajax({
    url: "./amazon_info",
    type: "GET",
    data: { title: title, author: author},
    dataType: 'json',
  }).done( function( data ){
    $('#quiz').append("<div id=amazon />")
    if ( data.image != null){
      $('#amazon').append("<a href=" + data.url + "  target=_blank><img src=" + data.image + " alt=" + data.title + "/></a>")
    }
    console.log("show_amazon_info: OK" + data);
  }).fail( function(XMLHttpRequest, textStatus, errorThrown) {
      console.log("show_amazon_info: NG " + textStatus);
  });
}

function begin_question(){
  console.log("begin_question");
  $('#book_table').remove();

  var title = $(this).children(":first-child").text()
  var author = $(this).children(":nth-child(2)").text()
  var question_id = $(this).attr("id")
  console.log(title);

  show_amazon_info(title, author);
  
  var $div = $('<div id=quiz />');
  $div.append("<div id=quiz_title><h1>「 " + title + " 」   "+ author + "</h1></div>");
  add_question($div, "<p>犯人は誰？</p>", question_id)
  
  $('#bottom').append($div);

}

function add_question(parent, question, question_id){
  var $div = $('<div class=question />');
  $div.append(question);
  $div.append('<input type=text class=answer_box />');
  var $answer_button = $('<input class=answer_button type=submit value=回答する question_id='+ question_id+ ' />')
  $div.append($answer_button)
  $answer_button.click( reply_answer );
  parent.append($div);
}

function reply_answer(){
  console.log("reply_answer");
  input_answer = $(this).prev().val()
  
  $.ajax({
    url: "./check_answer",
    type: "POST",
    data: { question_id: $(this).attr("question_id"), input_answer: input_answer},
    dataType: 'json',
    success: function(arr) {
      //var result = JSON.parse(arr);
      console.log("input_answer: OK" + arr.result);
      if(!arr.result){
        correct_answer(arr);
      } else {
        correct_answer(arr);
      }
    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
      console.log("input_answer: NG " + textStatus);
    }
  });
}

function correct_answer(arr){
  var button = $(".answer_button:last")
  button.attr("disabled", true)
  button.prev().attr("disabled", true);  //to disable text box
  button.parent().append('<span>ご名答...</span>')
  if(arr.next == 0 || arr.next == null){
    $(".question:last").after('<p>QED.</p>')
  } else {
   // TODO： 次の質問
  }
}

function clickTableHandler(event){
  console.log("clickTableHandler" + event);
}