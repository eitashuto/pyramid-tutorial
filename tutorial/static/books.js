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
function updateBooklist( booklist )
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
};

var val_book_hint = "";

function refrect_hint(){
  console.log("function refrect_hint");
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