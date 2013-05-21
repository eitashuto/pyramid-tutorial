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

//jQuery(function($) {
//  $('tr').addClass('clickable');
//  .click(function(e)

