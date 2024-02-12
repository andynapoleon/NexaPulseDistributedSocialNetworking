<script>
  import Post from "./Post.svelte";

  // Sample array of post objects
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
    // Add more posts as needed
  ];
</script>

<div class="posts">
  {#each posts as { id, userName, postTime, content }}
    <Post {userName} {postTime} {content} />
  {/each}
</div>

<style>
  .posts {
    display: flex;
    flex-direction: column-reverse;
    justify-content: space-between;
  }
</style>
