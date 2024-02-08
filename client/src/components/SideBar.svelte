<script>
  export let items = []; // expects an array of items for the sidebar
  import { Link } from "svelte-routing";
</script>

<aside class="sidebar">
  <nav>
    <ul>
      {#each items as item}
        <li>
          <div class="menu-item flex justify-right">
            <slot {item} />
            <a href={item.href}>{item.label}</a>
            <!-- <Link to={item.href}>{item.label}</Link> -->
          </div>
        </li>
      {/each}
    </ul>
  </nav>
</aside>

<style>
  .sidebar {
    width: 12%;
    height: 100vh;
    position: fixed;
    left: 0;
    top: 80px;
    padding-top: 1%;
    background-color: teal;
    box-shadow: 2px 0 5px rgba(0, 0, 0, 0.1);
    font-size: large;
    font-weight: bold;
  }

  nav ul {
    list-style: none;
    padding: 0;
    margin: 0;
  }

  nav li a {
    padding: 14px 12px;
    text-decoration: none;
    color: white;
  }

  .menu-item {
    padding-left: 5%;
  }

  nav li :hover {
    background-color: #1dc2ae;
  }
</style>
