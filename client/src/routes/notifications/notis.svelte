<script>
  import Post from "./noti.svelte";

  // Sample array of post objects - will do data fetching instead
  export let followRequests = [];
</script>

<div class="posts">
  {#each followRequests as { id, profileImageUrl, userName, postTime, content } (id)}
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
