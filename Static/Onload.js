 function dragStart(ev) {
    ev.dataTransfer.effectAllowed='move';
    ev.dataTransfer.setData("Text", ev.target.getAttribute('id'));
    ev.dataTransfer.setDragImage(ev.target,100,100);

    return true;
 }
 function dragEnter(ev) {
    ev.preventDefault();
    return true;
 }

 function dragOver(ev) {
    ev.preventDefault();
 }

 function dragDrop(ev) {
    var src = ev.dataTransfer.getData("Text");
    ev.target.appendChild(document.getElementById(src));
    ev.stopPropagation();
    return false;
 }
