<script>
  import UserImage from "../../components/UserImage.svelte";
  import Posts from "../../widgets/Posts.svelte";
</script>

<main class="posts">
  <h1 class="text-rose-600 font-bold text-xl">Community Posts</h1>
  <br />
  <Posts />
</main>

<style>
  .posts {
    padding-top: 10%;
    padding-left: 20%;
    padding-right: 7%;
  }
</style>
