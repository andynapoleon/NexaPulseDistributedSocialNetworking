<script>
  import CreatePost from "../../widgets/CreatePost.svelte";
  import Posts from "../../widgets/Posts.svelte";
  import { onMount } from "svelte";
  import {
    authToken,
    isLoginPage,
    getCurrentUser,
    currentUser,
    server,
  } from "../../stores/stores.js";
  import { fetchWithRefresh } from "../../utils/apiUtils.js";
  import { get } from "svelte/store";
  // let isAuthenticated = false;

  onMount(() => {
    $isLoginPage = false;
    console.log(getCurrentUser());
    console.log(get(authToken));

    // check if the github link is valid
    if (isValidGitHubLink(getCurrentUser().github)){
      // get the github username from the link
      const githubUsername = getGitHubUsername(getCurrentUser().github);
      // get 5 public events of the user from github 
      const response_github = fetch(
        `https://api.github.com/users/${githubUsername}/events/public?per_page=5`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
          },
        }
      ).then((response) => response.json())
      .then((data) => {
        // filter data by created_at and get the new activity since 
        data.forEach((event) => console.log("Past: ", new Date(event.created_at)));
        const lastUpdated = new Date(getCurrentUser().lastUpdated);
        console.log("Last Updated: ", getCurrentUser().lastUpdated);
        console.log("Threshold: ", lastUpdated);

        const newActivity = data.filter((event) => new Date(event.created_at) > lastUpdated);
        
        console.log("github", newActivity);

        // if there is new activity, create a new post for each activity
        if (newActivity.length > 0) {
          console.log("new activity", newActivity);
          newActivity.forEach((event) => {
            const postData = {
              authorId: getCurrentUser().userId,
              type: "post",
              title: `New ${event.type} event on GitHub!`,
              content: `${event.repo.name}: ${event.payload.commits && event.payload.commits.length > 0 ? event.payload.commits[0].message : ''}`,
              content_type: "text/markdown",
              visibility: "Public".toUpperCase(),
            };
            fetchWithRefresh(
              server + `/api/authors/${getCurrentUser().userId}/posts/`,
              {
                method: "POST",
                headers: {
                  Authorization: `Bearer ${get(authToken)}`,
                  "Content-Type": "application/json",
                },
                body: JSON.stringify(postData),
              }
            ).then((response) => {
              if (response.ok) {
                console.log("Post created successfully");
              } else {
                console.error("Failed to create post:", response.statusText);
              }
            });
          });     
          fetchPosts();
          // get the latest event and update the lastUpdated field
          const latestEvent = newActivity[0];
          // set the lastUpdated field to the latest event
          currentUser.update(user => {
            return { ...user, lastUpdated: latestEvent.created_at };
          });
          console.log("Updated lastUpdated: ", getCurrentUser().lastUpdated);
        } 
      });
    }
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

  // Function to fetch posts from the backend
  async function fetchPosts() {
    try {
      const response = await fetch(server + "/api/public-posts/", {
        method: "GET",
        headers: {
          Authorization: `Bearer ${$authToken}`,
        },
      });
      if (response.ok) {
        const data = await response.json();
        console.log("Fetched posts:", data); // Log the fetched data
        posts = data;
      } else {
        console.error("Failed to fetch posts:", response.statusText);
      }
    } catch (error) {
      console.error("Error fetching posts:", error.message);
    }
  }
  
  function isValidGitHubLink(link) {
    // Regular expression to match GitHub user profile URLs
    var regex = /^(https?:\/\/)?(www\.)?github\.com\/[a-zA-Z0-9_-]+$/;
    return regex.test(link);
  }

  function getGitHubUsername(link) {
    // Regular expression to match GitHub user profile URLs and extract the username
    var regex = /^(?:https?:\/\/)?(?:www\.)?github\.com\/([a-zA-Z0-9_-]+)$/;
    var match = link.match(regex);
    if (match) {
        return match[1]; // Return the username captured by the regex
    } else {
        return null; // Return null if the link is not a valid GitHub link
    }
  }
</script>

<main class="posts">
  <h1 class="text-[#0f6460] font-bold text-xl">Let's Create A Post!</h1>
  <br />
  <CreatePost/>
  <h1 class="text-[#0f6460] font-bold text-xl">Explore New Posts</h1>
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
