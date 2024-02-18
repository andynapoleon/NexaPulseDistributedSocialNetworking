<script>
  import Posts from "../../widgets/Posts.svelte";
  import ProfileWidget from "./ProfileWidget.svelte";
  export let id = null;

  // Fetch names & posts with the userId passed in
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
</script>

<main class="main">
  <div class="profile-layout">
    <div class="profile-widget">
      <ProfileWidget
        profileImageUrl="../../../fake_profile.png"
        name="Jane Smith"
        email="jane.smith@example.com"
        userId={id}
      />
    </div>
    <div class="posts">
      <Posts {posts} />
    </div>
  </div>
</main>

<style>
  .main {
    padding-top: 10%;
    padding-left: 20%;
    padding-right: 7%;
  }

  .profile-layout {
    display: flex;
    justify-content: space-between;
    gap: 2rem; /* Adjust the gap as needed */
  }

  .profile-widget {
    flex: 1; /* Adjust the flex basis as needed */
    max-width: 300px; /* Adjust the width as needed */
  }

  .posts {
    flex: 3; /* Adjust the flex basis as needed */
  }
</style>
