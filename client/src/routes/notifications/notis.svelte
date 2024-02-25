<script>
  import Post from "./noti.svelte";
  export let followRequests = [];
</script>

<div class="posts">
  {#each followRequests as { id, userId, profileImageUrl, userName, postTime, content } (id)}
    <Post {userId} {profileImageUrl} {userName} {postTime} {content}/>
  {/each}
</div>

<style>
  .posts {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
</style>
