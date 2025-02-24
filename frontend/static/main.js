// Function that runs once the window is fully loaded
window.onload = function() {
    var savedBaseUrl = localStorage.getItem('apiBaseUrl');
    if (savedBaseUrl) {
        document.getElementById('api-base-url').value = savedBaseUrl;
        loadPosts();
    }
};

// Function to fetch all posts and display them
function loadPosts() {
    var baseUrl = document.getElementById('api-base-url').value;
    localStorage.setItem('apiBaseUrl', baseUrl);

    fetch(baseUrl + '/posts')
        .then(response => response.json())
        .then(data => displayPosts(data.posts))
        .catch(error => console.error('Error:', error));
}

// Function to display posts dynamically
function displayPosts(posts) {
    const postContainer = document.getElementById('post-container');
    postContainer.innerHTML = '';

    posts.forEach(post => {
        const postDiv = document.createElement('div');
        postDiv.className = 'post';

        postDiv.innerHTML = `
            <h2>${post.title}</h2>
            <p><strong>By:</strong> ${post.author} | <strong>Date:</strong> ${post.date}</p>
            <p>${post.content}</p>
            <button onclick="deletePost(${post.id})">🗑 Delete</button>
            <button onclick="likePost(${post.id})">👍 Like (<span id="like-count-${post.id}">0</span>)</button>
            <button onclick="toggleCommentSection(${post.id})">💬 Comment</button>
            <div id="comments-${post.id}" class="comments-section" style="display: none;">
                <input type="text" id="comment-input-${post.id}" placeholder="Write a comment..." />
                <button onclick="addComment(${post.id})">Submit</button>
                <div id="comment-list-${post.id}"></div>
            </div>
        `;

        postContainer.appendChild(postDiv);
    });
}

// Function to add a new post
function addPost() {
    var baseUrl = document.getElementById('api-base-url').value;
    var postTitle = document.getElementById('post-title').value;
    var postContent = document.getElementById('post-content').value;
    var postAuthor = document.getElementById('post-author').value;

    fetch(baseUrl + '/posts', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ title: postTitle, content: postContent, author: postAuthor })
    })
    .then(response => response.json())
    .then(post => {
        console.log('Post added:', post);
        loadPosts();
    })
    .catch(error => console.error('Error:', error));
}

// Function to delete a post
function deletePost(postId) {
    var baseUrl = document.getElementById('api-base-url').value;

    fetch(baseUrl + '/posts/' + postId, {
        method: 'DELETE'
    })
    .then(response => {
        console.log('Post deleted:', postId);
        loadPosts();
    })
    .catch(error => console.error('Error:', error));
}

// Function to like a post
function likePost(postId) {
    const likeCountElement = document.getElementById(`like-count-${postId}`);
    let currentLikes = parseInt(likeCountElement.innerText);
    likeCountElement.innerText = currentLikes + 1;
}

// Function to toggle comment section
function toggleCommentSection(postId) {
    const commentSection = document.getElementById(`comments-${postId}`);
    commentSection.style.display = commentSection.style.display === 'none' ? 'block' : 'none';
}

// Function to add a comment to a post
function addComment(postId) {
    const commentInput = document.getElementById(`comment-input-${postId}`);
    const commentText = commentInput.value.trim();
    if (commentText === '') return;

    const commentList = document.getElementById(`comment-list-${postId}`);
    const commentDiv = document.createElement('div');
    commentDiv.innerHTML = `<p>💬 ${commentText}</p>`;
    commentList.appendChild(commentDiv);

    commentInput.value = ''; // Clear input field after submitting
}

// Function to fetch sorted posts
function loadSortedPosts() {
    var baseUrl = document.getElementById('api-base-url').value;
    var sortOption = document.getElementById('sort-options').value;

    fetch(`${baseUrl}/posts?sort=${sortOption}&direction=desc`)
        .then(response => response.json())
        .then(data => displayPosts(data.posts))
        .catch(error => console.error('Error:', error));
}

// Function to search posts
function searchPosts() {
    var baseUrl = document.getElementById('api-base-url').value;
    var query = document.getElementById('search-query').value;

    fetch(`${baseUrl}/posts/search?query=${query}`)
        .then(response => response.json())
        .then(data => displayPosts(data))
        .catch(error => console.error('Error:', error));
}