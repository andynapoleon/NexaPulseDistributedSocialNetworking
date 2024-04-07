<script>
    import { fetchWithRefresh } from "../../utils/apiUtils.js";
    import { server, authToken } from "../../stores/stores.js";
    import { get } from "svelte/store";
  
    export let comment;
    export let authorId;
    export let postId;
  
    let commentLikeCount = 0;
    let isLiked = false;
  
    async function fetchCommentLikes() {
      try {
        console.log(`post id: ${postId} comment id: ${comment.id}`)
        const response = await fetchWithRefresh(
          `${server}/api/authors/${authorId}/posts/${postId}/comments/${comment.id}/listoflikes`,
          {
            method: "GET",
            headers: {
              Authorization: `Bearer ${get(authToken)}`,
            },
          }
        );
  
        if (response.ok) {
          const likes = await response.json();
          commentLikeCount = likes.length;
          isLiked = likes.some((like) => like.author.id === authorId);
        } else {
          console.error("Failed to fetch likes:", response.statusText);
        }
      } catch (error) {
        console.error("Error fetching likes:", error.message);
      }
    }
  
    async function toggleCommentLike() {
      try {
        if (isLiked) {
          // Unlike the comment
          const response = await fetchWithRefresh(
            `${server}/api/authors/${authorId}/comment/inbox`,
            {
              method: "DELETE",
              headers: {
                Authorization: `Bearer ${get(authToken)}`,
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ author: authorId, post: postId, comment: comment.id }),
            }
          );
  
          if (response.ok) {
            isLiked = false;
            fetchCommentLikes();
          } else {
            console.error("Failed to unlike the comment:", response.statusText);
          }
        } else {
          // Like the comment
          const response = await fetchWithRefresh(
            `${server}/api/authors/${authorId}/comment/inbox`,
            {
              method: "POST",
              headers: {
                Authorization: `Bearer ${get(authToken)}`,
                "Content-Type": "application/json",
              },
              body: JSON.stringify({ author: authorId, post: postId, comment: comment.id }),
            }
          );
  
          if (response.ok) {
            isLiked = true;
            fetchCommentLikes();
          } else {
            console.error("Failed to like the comment:", response.statusText);
          }
        }
      } catch (error) {
        console.error("Error toggling like:", error.message);
      }
    }

    fetchCommentLikes();
  </script>
  
  <div class="comment">
    <div>{comment.comment}</div>
  </div>

  <style>
    .comment {
      color: black; /* Set text color to black */
      margin-bottom: 10px; /* Add some spacing between comments */
    }
  
    .like-button {
      background-color: #007bff; /* Blue color */
      color: white;
      border: none;
      padding: 5px 10px;
      border-radius: 5px;
      cursor: pointer;
      margin-top: 5px;
    }
  </style>
  
  