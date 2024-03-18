<script>
  import Post from "./noti.svelte";
  export let followRequests = [];
</script>

<div class="posts">
  {#each followRequests as { id, userId, profileImage, userName, postTime, content } (id)}
    <Post {userId} {profileImage} {userName} {postTime} {content}/>
  {/each}
</div>

<style>
  .posts {
    display: flex;
    flex-direction: column;
    justify-content: space-between;
  }
</style>
