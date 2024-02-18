<script>
  import ProfileWidget from "./ProfileWidget.svelte";
  export let id = null;
</script>

<main class="main">
  <ProfileWidget
    profileImageUrl="../../../fake_profile.png"
    name="Jane Smith"
    email="jane.smith@example.com"
    favoriteGame="Final Fantasy VII"
    userId={id}
  />
</main>

<style>
  .main {
    padding-top: 10%;
    padding-left: 20%;
    padding-right: 7%;
  }
</style>
