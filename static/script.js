$(document).ready(function() {
    let sortableList = $("#sortable");

    // Function to update the IDs based on list order
    function updateListOrder() {
        // Select all list items in the sortable list
        const listItems = sortableList.find('li');

        // Iterate through the list items and update their IDs
        listItems.each(function(index) {
            $(this).attr('id', 'item-' + (index + 1));
        });
    }

    let itemOrder = [];

    // Initialize the sortable functionality
    sortableList.sortable({
        update: function(event, ui) {
            // Update the item order array when the list is sorted
            updateListOrder()
        }
    });

    // Handle saving the order
    $("#save-button").click(function() {
        console.log("Item Order:", itemOrder);
        returnData = readListItems();
        // Send a POST request to your server with the item order data
        fetch('/save-order', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(returnData)
        })
        .then(response => {
            if (response.ok) {
                // Handle successful response from the server
                console.log('Order saved successfully.');
            } else {
                // Handle error response from the server
                console.error('Failed to save order.');
            }
        })
        .catch(error => {
            // Handle network or other errors
            console.error('Error:', error);
        });
    });

    // Function to add a new item
    function addNewItem() {
        const addButton = document.querySelector(".add-button");
        const list = document.querySelector("#sortable");

        const newItem = document.createElement("li");
        newItem.textContent = "New Item";
        newItem.classList.add(
            "ui-sortable-handle", // For sorting
            "panel-item",
            "list-group-item",
            "d-flex",
            "justify-content-between",
            "lh-condensed",
            "rounded-lg",
            "my-2"
        );
        newItem.setAttribute("onClick", "editItem(this)");
        
        newItem.id = "item-" + (list.children.length + 1);
        list.insertBefore(newItem, addButton);
        updateListOrder();
    }

    // Attach a click event to the "Add Item" button
    document.querySelector(".add-button").addEventListener("click", function() {
        addNewItem();
    });

    updateListOrder(); // Call to initially set the IDs
});

function readListItems() {
    var listItems = document.querySelectorAll('ul li'); // Select all <li> elements inside the <ul>
    var itemList = [];

    listItems.forEach(function(item) {
        var id = item.id;
        var text = item.textContent;
        itemList.push({ id, text });
    });

    return itemList;
}
