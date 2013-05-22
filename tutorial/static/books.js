function updateBooklist2( booklist )
{
  for(var i=0; i<booklist.length; i++) {
  book = booklist[i]
    $("#book_list").append(
      $('<tr>').append(
        $('<td class="title">').text(book.title)
      ).append(
        $('<td class="author">').text(book.author)
      )
    );
  };
};

google.load('visualization', '1', {packages:['table']});

//Visualization: Table
function updateBooklist3( booklist )
{
    var data = new google.visualization.DataTable();
    data.addColumn('string', '題名');
    data.addColumn('string', '著者');
    
    for(var i=0; i<booklist.length; i++) {
      book = booklist[i]
      data.addRows([
        [book.title, book.author]
     ]);
    };
   var table = new google.visualization.Table(document.getElementById('book_list'));
   table.draw(data, {showRowNumber: true});
   google.visualization.events.addListener(table, 'select', clickTableHandler);
};

function updateBooklist( booklist )
{
  console.log("updateBooklist");
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

function begin_question(){
  console.log("begin_question");
  $('#book_table').remove();

  console.log($(this))
  var title = $(this).children(":first-child").text()
  var author = $(this).children(":nth-child(2)").text()
  var question_id = $(this).attr("id")
  console.log(title);

  var $div = $('<div/>');
  $div.append("<h1>「 " + title + " 」   "+ author + "</h1>");
  add_question($div, "<p>犯人は誰？</p>", question_id)
  
  //$div.append("<p>犯人は誰？</p>");
  //$div.append("<input type=\"text\"/><input type=\"submit\" value=\"回答する\" id=\"input_answer\"/>");
  $('#bottom').append($div);

}

function add_question(parent, question, question_id){
  var $div = $('<div/>');
  $div.append(question);
  $div.append('<input type=\"text\"/>');
  var $answer_button = $('<input type=\"submit\" value=\"回答する\" id='+ question_id+ '/>')
  $div.append($answer_button)
  $answer_button.click( input_answer );
  parent.append($div);
}

function input_answer(){
  console.log("input_answer");
  input_answer = $(this).prev().val()
  
  $.ajax({
    url: "./check_answer",
    type: "POST",
    data: { question_id: $(this).attr("id"), input_answer: input_answer},
    dataType: 'json',
    success: function(arr) {
      //var result = JSON.parse(arr);
      console.log("input_answer: OK" + arr.result);
    },
    error: function(XMLHttpRequest, textStatus, errorThrown) {
      console.log("input_answer: NG " + textStatus);
    }
  });
}

function clickTableHandler(event){
  console.log("clickTableHandler" + event);
}