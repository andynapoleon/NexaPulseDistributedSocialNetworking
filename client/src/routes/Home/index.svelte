<script>
  import CreatePost from "../../widgets/CreatePost.svelte";
  import Posts from "../../widgets/Posts.svelte";

  // Array to hold post objects
  let posts = [
    {
      id: 1,
      userName: "John Doe",
      postTime: "1h ago",
      content: "This is my first post!",
    },
    {
      id: 2,
      userName: "Jane Smith",
      postTime: "2h ago",
      content: "Svelte is awesome!",
    },
    {
      id: 3,
      userName: "Dave Lee",
      postTime: "3h ago",
      content: "Check out my new project.",
    },
  ];

  // Function to handle the creation of a new post
  function handleCreatePost(event) {
    const newPost = {
      id: posts.length + 1, // Simple ID assignment; consider a more robust ID generation strategy
      userName: "Current User", // Placeholder; use actual user data in a real app
      postTime: "Just now",
      content: event.detail.content,
    };
    posts = [newPost, ...posts]; // Add the new post to the beginning of the posts array
  }
</script>

<main class="posts">
  <h1 class="text-[#0f6460] font-bold text-xl">Let's Create A Post!</h1>
  <br />
  <CreatePost on:createpost={handleCreatePost} />
  <h1 class="text-[#0f6460] font-bold text-xl">Community Posts</h1>
  <br />
  <Posts {posts} />
</main>

<style>
  .posts {
    padding-top: 10%;
    padding-left: 20%;
    padding-right: 7%;
  }
</style>
