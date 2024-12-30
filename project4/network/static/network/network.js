function like(id) {
    // Fetch post by id
    fetch(`/like/${id}`)
    .then(response => response.json())
    .then(result => {

        console.log(result)

        if (result.message == "liked") {
            // Update like count and button content
            document.getElementById(`like_${id}`).innerHTML = 'Unlike';
            document.getElementById(`like_count_${id}`).innerHTML = `&#x2665;&#xfe0f; ${result.like_count}`;

        } else {
            // Update like count and button content
            document.getElementById(`like_${id}`).innerHTML = 'Like';
            document.getElementById(`like_count_${id}`).innerHTML = `&#x2665;&#xfe0f; ${result.like_count}`;
        };
    });
}

function cancel_edit(id) {
    // Hide edit form and remove textarea
    document.getElementById(`edit_fields ${id}`).hidden = true;
    document.getElementById(`edit_textarea ${id}`).innerHTML = '';

    // Display previous post content and edit button
    document.getElementById(`content ${id}`).hidden = false;
    document.getElementById(`edit_button ${id}`).hidden = false;
}

function save_edit(id) {
    // Get CSRF token and save updated content
    const csrfToken = document.getElementById(`save ${id}`).getAttribute('data-csrf');
    new_content = document.getElementById(`new_content ${id}`).value

    fetch(`/edit/${id}`, {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrfToken
          },
        body: JSON.stringify( {
            content: new_content
        })
    })
    .then(response => response.json())
    .then(post => {

            // Hide edit form and remove textarea
            document.getElementById(`edit_fields ${post.id}`).hidden = true;
            document.getElementById(`edit_textarea ${post.id}`).innerHTML = '';

            // Display new post content and edit button
            document.getElementById(`content ${post.id}`).innerHTML = `${post.content}`;
            document.getElementById(`content ${post.id}`).hidden = false;
            document.getElementById(`edit_button ${post.id}`).hidden = false;
    });
}

function edit_post(id) {
    // Fetch post by id
    fetch(`/edit/${id}`)
    .then(response => response.json())
    .then(post => {

        // Display edit form and add textarea with current post content
        document.getElementById(`edit_fields ${post.id}`).hidden = false;
        document.getElementById(`edit_textarea ${post.id}`).innerHTML = `<textarea autofocus name="content" id="new_content ${post.id}" rows="3" cols="120">${post.content}</textarea>`;

        // Hide exisitng post content and edit button
        document.getElementById(`content ${post.id}`).hidden = true;
        document.getElementById(`edit_button ${post.id}`).hidden = true;

        // Add on click listener to cancel and save buttons
        document.getElementById(`cancel ${post.id}`).addEventListener('click', () => cancel_edit(`${post.id}`));
        document.getElementById(`save ${post.id}`).addEventListener('click', () => save_edit(`${post.id}`));
    });
}
