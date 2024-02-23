<script>
  export let id;
  import Notis from "./notis.svelte";
  import { onMount } from "svelte";
  import { server, authToken, getCurrentUser } from "../../stores/stores.js";
  import { get } from "svelte/store";

  // Define an array to store follow requests
  let followRequests = [];

  onMount(async () => {
    const followRequestsEndpoint = server + `/api/follow/${getCurrentUser().userId}/all/`;
    const response = await fetch(followRequestsEndpoint, {
      method: "GET",
      headers: {
        'Authorization': `Bearer ${get(authToken)}`, // Include the token in the request headers
      }
    });

    if (!response.ok) {
      throw new Error("Failed to fetch follow requests");
    }

    const data = await response.json();
    console.log(data)

    // create an array from fetched requests
    for (let i = 0; i < data.followRequests.length; i++) {
      followRequests.push({
        id: data.followRequests[i].id,
        profileImageUrl:
          "https://seeded-session-images.scdn.co/v2/img/122/secondary/artist/4tmoBDLDleElXopuhDljGR/en",
        userName: "John Doe",
        postTime: "1h ago",
      })
    }
  });

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
      <Notis {followRequests} />
    </div>
  </div>
</main>

<style>
  @import "notiStyle.css";
</style>
