function parse_page(){
    let params = new URL(document.location.toString()).searchParams;
    var dept = params.get("departmentDisplayName");
    var course = params.get("courseDisplayName");
    var section = params.get("sectionDisplayName");
    var progid = params.get("programId");
    var mat = document.querySelectorAll('div.materials-info');
    var data = [];
    var binfo = [];
    if (mat.length == 0){
       // search for no books
       var nb = document.querySelector('span.course-notice');
       if (nb.innerText == 'No books required for this course.'){
           var title = 'NO BOOKS FOR COURSE';
       } else if (nb.innerText == 'We are unable to find the specified course.'){
           var title = 'UNABLE TO FIND COURSE';
       } else {
           var title = nb.innerText;
       }
       binfo.push(dept);
       binfo.push(course);
       binfo.push(section);
       binfo.push(progid);
       binfo.push(title);
       data.push(binfo);
    }
    // Iterate over the elements
    mat.forEach(div => {
        var binfo = [];
        var title = div.previousElementSibling.innerText;
        var req = div.previousElementSibling.previousElementSibling.querySelector('span');
        if (req) {
             var req_text = req.innerText;
        }
        else if (!req) {
            // optional
            var opt = div.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement.parentElement;
            var seln = opt.querySelector('span.choose-materials-prompt').innerText;
            var rn = opt.querySelector('div').querySelector('span').innerText;
            var req_text = rn + " " + seln;
        }
        try {
            var hdiv = div.parentElement.parentElement.parentElement;
            var qp = hdiv.querySelectorAll('span.purchase-option-item-price');
            var qt = hdiv.querySelectorAll('h6.purchase-option-item-title');
            var price_text = '';
            for (let i = 0; i < qp.length; i++){
                price_text = price_text + qt[i].innerText + " " + qp[i].innerText + ", ";
            }
        } catch (error) {
            var price = div.querySelector('span.text-overflow');
            var price_text = price.textContent;
        }
        var il = div.querySelector('ol.info-list').querySelectorAll('li');
        binfo.push(dept);
        binfo.push(course);
        binfo.push(section);
        binfo.push(progid);
        binfo.push(title);
        binfo.push(req_text);
        binfo.push(price_text);
        for (let i = 0; i < il.length; i++){
            binfo.push(il[i].innerText);
        }
        data.push(binfo)
    });
    return data;
}

function arrayToTable(array){
    const table = document.createElement('table')
    for (let i = 0; i < array.length; i++){
        const row = table.insertRow();
        ar = array[i];
        for (j = 0; j < ar.length; j++){
          const cell = row.insertCell();
          cell.textContent = ar[j];
        }
    }
    table.setAttribute("class","mytable");
    return table
};

function selectElementContents(el) {
  var body = document.body,
    range, sel;
  if (document.createRange && window.getSelection) {
    range = document.createRange();
    sel = window.getSelection();
    sel.removeAllRanges();
    range.selectNodeContents(el);
    sel.addRange(range);
  }
  document.execCommand("Copy");
}


//console.log('The extension works');

function run(){
  var d = parse_page();
  var tb = arrayToTable(d);
  console.log(tb);
  document.body.appendChild(tb);
  tb2 = document.querySelector('table.mytable');
  selectElementContents(tb2);
  //window.alert("Table copied");
  tb2.remove();
}

document.addEventListener('keydown', (event) => {
  if (event.key === 'Enter'){
      run();
  }
});