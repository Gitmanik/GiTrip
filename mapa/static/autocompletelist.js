function populateList(el_id, id, data, func_name)
{
    clearAllLists();

    for (let i of data) {

        let listItem = document.createElement("li");

        listItem.classList.add("list-items");
        listItem.style.cursor = "pointer";
        listItem.style['z-index'] = 100000;
        listItem.setAttribute("onclick", func_name + "(`" + el_id + "`, `" + i + "`)");

        listItem.innerHTML = i;
        document.querySelector("#" + id).appendChild(listItem);
    }
}

function clearAllLists()
{
      let items = document.querySelectorAll('.list-items');
      items.forEach((item) => {
        item.remove();
      });
}