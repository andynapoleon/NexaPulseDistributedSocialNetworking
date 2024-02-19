<script>
  import Post from "./noti.svelte";

  // Sample array of post objects - will do data fetching instead
  export let posts = [];
</script>

<div class="posts">
  {#each posts as { id, profileImageUrl, userName, postTime, content } (id)}
    <Post {profileImageUrl} {userName} {postTime} {content}/>
  {/each}
</div>

<style>
  .posts {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
</style>
