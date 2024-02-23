<script>
  import CreatePost from "../../widgets/CreatePost.svelte";
  import Posts from "../../widgets/Posts.svelte";
  import { onMount } from "svelte";
  import { authToken, isLoginPage, getCurrentUser, server } from "../../stores/stores.js";
  import { fetchWithRefresh } from "../../utils/apiUtils.js";
  import { get } from "svelte/store";
  // let isAuthenticated = false;

  onMount(() => {
    $isLoginPage = false;
    // isAuthenticated = $authToken !== "";
    // console.log(isAuthenticated);
    // if (!isAuthenticated) {
    //   $isLoginPage = true;
    //   navigate("/");
    // }
  });

  // Array to hold post objects
  let posts = [
    {
      id: 1,
      userName: "John Doe",
      postTime: "1h ago",
      title: "First Post",
      content: "This is my first post!",
      visibility: "Public",
    },
    {
      id: 2,
      userName: "Jane Smith",
      postTime: "2h ago",
      title: "Svelte",
      content: "Svelte is awesome!",
      visibility: "Public",
    },
    {
      id: 3,
      userName: "Dave Lee",
      postTime: "3h ago",
      title: "New Project",
      content: "Check out my new project.",
      visibility: "Public",
    },
  ];

  // Function to handle the creation of a new post
  async function handleCreatePost(event) {
    let newPost = {
      userName: getCurrentUser().name, // Placeholder; use actual user data in a real app
      postTime: "Just now",
      title: event.detail.title,
      content: event.detail.content,
      visibility: event.detail.visibility,
    };
    // fetch api here 
    const createPostEndpoint = server + `service/api/authors/${getCurrentUser().userId}/posts/`;
    const response = await fetchWithRefresh(createPostEndpoint, {
        method: "POST",
        headers: {
      'Authorization': `Bearer ${get(authToken)}`, // Include the token in the request headers
      'Content-Type': 'application/json'
    },
      body: JSON.stringify(newPost),
    });
    if (!response.ok) {
      throw new Error("Failed to fetch follow status");
    }
    const post = await response.json();
    posts = [post, ...posts]; // Add the new post to the beginning of the posts array
  }
</script>

<main class="posts">
  <h1 class="text-[#0f6460] font-bold text-xl">Let's Create A Post!</h1>
  <br />
  <CreatePost on:createpost={handleCreatePost} />
  <h1 class="text-[#0f6460] font-bold text-xl">Community Posts</h1>
  <br />
  <Posts {posts} />
</main>

<style>
  .posts {
    padding-top: 7%;
    padding-left: 20%;
    padding-right: 7%;
  }
</style>
