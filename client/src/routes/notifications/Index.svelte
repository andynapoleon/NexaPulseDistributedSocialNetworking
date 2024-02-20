<script>
  export let id;
  import Notis from "./notis.svelte";

  let posts = [
    {
      id: 1,
      profileImageUrl:
        "https://seeded-session-images.scdn.co/v2/img/122/secondary/artist/4tmoBDLDleElXopuhDljGR/en",
      userName: "John Doe",
      postTime: "1h ago",
    },
    {
      id: 2,
      profileImageUrl:
        "https://seeded-session-images.scdn.co/v2/img/122/secondary/artist/4tmoBDLDleElXopuhDljGR/en",
      userName: "Jane Smith",
      postTime: "2h ago",
    },
    {
      id: 3,
      profileImageUrl:
        "https://seeded-session-images.scdn.co/v2/img/122/secondary/artist/4tmoBDLDleElXopuhDljGR/en",
      userName: "Dave Lee",
      postTime: "3h ago",
    },
  ];
</script>

<main class="main" {id}>
  <div class="profile-layout">
    <div class="profile-widget"></div>
    <div class="posts">
      <Notis {posts} />
    </div>
  </div>
</main>

<style>
  @import "notiStyle.css";
</style>
