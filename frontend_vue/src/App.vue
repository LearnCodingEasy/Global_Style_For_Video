<script setup>
import { RouterLink, RouterView, useRouter } from 'vue-router'
import axios from 'axios'
import { onMounted, ref } from 'vue'
import { useUserStore } from '@/stores/user'
const router = useRouter()
const userStore = useUserStore()
// للتحكم في القائمة المنسدلة
const isDropdownOpen = ref(false)
const toggleDropdown = () => {
  isDropdownOpen.value = !isDropdownOpen.value
}
const closeDropdown = () => {
  isDropdownOpen.value = false
}
// تسجيل الخروج
const logout = async () => {
  console.log('ضغطت على تسجيل الخروج')
  try {
    await userStore.logout()
    console.log(` تم تسجيل الخروج بنجاح`)
  } catch (error) {
    console.log(` حصل خطأ أثناء تسجيل الخروج`)
    console.error(error)
  } finally {
    // مسح البيانات محليًا
    userStore.removeToken()
    router.push('/login')
  }
}
onMounted(() => {
  userStore.initStore()
  const token = userStore.user.access
  axios.defaults.headers.common['Authorization'] = token ? `Bearer ${token}` : ''
  if (!token) router.push('/login')
})
</script>

<template>
  <div class="wrapper_page_app">
    <div class="header_wrapper sticky top-0 left-0 right-0">
      <div class="container mx-auto">
        <div class="header_inner">
          <prime_card class="header_card px-2" v-if="userStore.user.isAuthenticated">
            <template #content>
              <header class="header_header">
                <nav class="header_nav">
                  <div class="header_content">
                    <div class="header_content_inner relative flex items-center justify-between">
                      <div
                        class="header_mobile_menu_button absolute inset-y-0 left-0 flex items-center sm:hidden"
                      >
                        <button
                          type="button"
                          class="relative inline-flex items-center justify-center rounded-md p-2 text-gray-400 hover:bg-blue-600 hover:text-white focus:outline-none focus:ring-2 focus:ring-inset focus:ring-white"
                          aria-controls="mobile-menu"
                          aria-expanded="false"
                        >
                          <span class="absolute -inset-0.5"></span>
                          <span class="sr-only">Open main menu</span>

                          <svg
                            class="block h-6 w-6"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke-width="1.5"
                            stroke="currentColor"
                            aria-hidden="true"
                            data-slot="icon"
                          >
                            <path
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              d="M3.75 6.75h16.5M3.75 12h16.5m-16.5 5.25h16.5"
                            />
                          </svg>

                          <svg
                            class="hidden h-6 w-6"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke-width="1.5"
                            stroke="currentColor"
                            aria-hidden="true"
                            data-slot="icon"
                          >
                            <path
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              d="M6 18 18 6M6 6l12 12"
                            />
                          </svg>
                        </button>
                      </div>
                      <div
                        class="header_wrapper_links flex flex-1 items-center justify-center sm:items-stretch sm:justify-start"
                      >
                        <div class="header_logo_link flex flex-shrink-0 items-center">
                          <RouterLink to="/" class="logo flex">
                            <span class=""> Work Remotely </span>
                          </RouterLink>
                        </div>
                        <div class="header_main_links hidden sm:ml-6 sm:block">
                          <div class="header_main_link flex space-x-4">
                            <RouterLink
                              to="/Vendors"
                              class="rounded-md px-3 py-2 text-md"
                              aria-current="page"
                            >
                              Vendors</RouterLink
                            >
                            <RouterLink to="/about" class="rounded-md px-3 py-2 text-md"
                              >About
                            </RouterLink>
                            <RouterLink to="/products" class="rounded-md px-3 py-2 text-md"
                              >Products
                            </RouterLink>
                          </div>
                        </div>
                      </div>
                      <div
                        class="header_wrapper_profile_search absolute inset-y-0 right-0 flex items-center pr-2 sm:static sm:inset-auto sm:ml-6 sm:pr-0"
                      >
                        <div class="header_input_search">
                          <prime_input_text></prime_input_text>
                        </div>
                        <button
                          type="button"
                          class="relative rounded-full bg-gray-800 p-1 text-gray-400 hover:text-white focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800"
                        >
                          <span class="absolute -inset-1.5"></span>
                          <span class="sr-only">View notifications</span>
                          <svg
                            class="h-6 w-6"
                            fill="none"
                            viewBox="0 0 24 24"
                            stroke-width="1.5"
                            stroke="currentColor"
                            aria-hidden="true"
                            data-slot="icon"
                          >
                            <path
                              stroke-linecap="round"
                              stroke-linejoin="round"
                              d="M14.857 17.082a23.848 23.848 0 0 0 5.454-1.31A8.967 8.967 0 0 1 18 9.75V9A6 6 0 0 0 6 9v.75a8.967 8.967 0 0 1-2.312 6.022c1.733.64 3.56 1.085 5.455 1.31m5.714 0a24.255 24.255 0 0 1-5.714 0m5.714 0a3 3 0 1 1-5.714 0"
                            />
                          </svg>
                        </button>
                        <div class="relative ml-3">
                          <div>
                            <button
                              type="button"
                              class="relative flex rounded-full bg-gray-800 text-sm focus:outline-none focus:ring-2 focus:ring-white focus:ring-offset-2 focus:ring-offset-gray-800"
                              id="user-menu-button"
                              aria-expanded="false"
                              aria-haspopup="true"
                              @click="toggleDropdown"
                            >
                              <span class="absolute -inset-1.5"></span>
                              <span class="sr-only">Open user menu</span>
                              <img
                                v-if="userStore.user.get_avatar !== 'undefined'"
                                :src="userStore.user.get_avatar"
                                class="h-8 w-8 rounded-full"
                                alt=""
                              />
                              <img
                                v-else
                                class="h-8 w-8 rounded-full"
                                src="https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80"
                                alt=""
                              />
                            </button>
                          </div>
                          <!-- dropdown -->
                          <div
                            v-if="isDropdownOpen"
                            class="border absolute right-0 z-10 mt-2 w-48 origin-top-right rounded-md py-1 shadow-lg ring-1 ring-black ring-opacity-5 focus:outline-none"
                            role="menu"
                            aria-orientation="vertical"
                            aria-labelledby="user-menu-button"
                            tabindex="-1"
                          >
                            <!-- User Profile -->
                            <div class="div_wrapper_profile flex py-1 items-center cursor-pointer">
                              <div
                                class="icon_div_wrapper_profile flex justify-center items-center"
                              >
                                <RouterLink
                                  class="flex justify-center items-center"
                                  v-if="userStore.user.id"
                                  :to="{
                                    name: 'profile',
                                    params: { id: userStore.user.id },
                                  }"
                                  @click="closeDropdown"
                                >
                                  <!-- If Image -->
                                  <div class="mr-1">
                                    <span
                                      class="user_img"
                                      v-if="userStore.user.get_avatar !== 'undefined'"
                                    >
                                      <img
                                        :src="userStore.user.get_avatar"
                                        class="rounded-full w-8 h-8"
                                        alt=""
                                      />
                                    </span>
                                    <span class="user_icon" v-else>
                                      <i class="pi pi-user px-2" shape="circle"></i>
                                    </span>
                                  </div>
                                  <!-- If Name -->
                                  <div class="">
                                    <span class="user_name" v-if="userStore.user.name">{{
                                      userStore.user.name
                                    }}</span>
                                    <span class="user_name" v-else>Your Profile</span>
                                  </div>
                                </RouterLink>
                              </div>
                            </div>
                            <!-- Settings -->
                            <div class="div_wrapper_logout flex py-1 items-center cursor-pointer">
                              <div
                                class="icon_logout flex justify-center items-center"
                                @click="closeDropdown"
                              >
                                <i class="pi pi-cog px-2" shape="circle"></i>
                                <button class="">Settings</button>
                              </div>
                            </div>
                            <!-- Sign Out -->
                            <div
                              class="div_wrapper_logout flex py-1 items-center cursor-pointer"
                              @click="logout"
                            >
                              <div
                                class="icon_logout flex justify-center items-center"
                                @click="closeDropdown"
                              >
                                <i class="pi pi-sign-out px-2" shape="circle"></i>
                                <button class="">Sign out</button>
                              </div>
                            </div>
                            <!-- Toggle Theme -->
                            <div
                              class="flex div_wrapper_toggle_theme cursor-pointer"
                              @click="closeDropdown"
                            >
                              <ThemeSwitcher />
                              <span class="mb-2">Toggle theme</span>
                            </div>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>

                  <div class="sm:hidden" id="mobile-menu">
                    <div class="space-y-1 px-2 pb-3 pt-2">
                      <a
                        href="#"
                        class="block rounded-md bg-gray-900 px-3 py-2 text-base font-medium text-white"
                        aria-current="page"
                        >Dashboard</a
                      >
                      <a
                        href="#"
                        class="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-gray-700 hover:text-white"
                        >Team</a
                      >
                      <a
                        href="#"
                        class="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-gray-700 hover:text-white"
                        >Projects</a
                      >
                      <a
                        href="#"
                        class="block rounded-md px-3 py-2 text-base font-medium text-gray-300 hover:bg-gray-700 hover:text-white"
                        >Calendar</a
                      >
                    </div>
                  </div>
                </nav>
              </header>
            </template>
          </prime_card>
        </div>
      </div>
    </div>
    <prime_toast />

    <RouterView />
  </div>
</template>

<script>
export default {
  setup() {
    return {}
  },
  data() {
    return {
      // تعريف الخاصية
    }
  },
  mounted() {
    document.title = 'Home'
  },
  computed: {},
  methods: {},
}
</script>

<style lang="scss">
.header_right_section {
  a,
  RouterLink {
    margin: 0 0.5rem;
  }
}

.wrapper_page_app {
  .header_wrapper {
    border-bottom: 1px solid #99999985;
    z-index: 7;
    .container {
      .header_inner {
        .header_card {
          border-radius: 0;
          box-shadow: none;

          > div {
            padding: 0;

            header.header_header {
              nav.header_nav {
                .header_content {
                  .header_content_inner {
                    .header_mobile_menu_button {
                      button {
                        border: 0.1rem solid #085dd8;
                      }
                    }

                    .header_wrapper_links {
                      .header_logo_link {
                        .logo {
                          i {
                          }
                        }
                      }

                      .header_main_links {
                        .header_main_link {
                          a {
                          }

                          button {
                            background-color: #085dd8;
                            border: 0;
                            color: white;
                          }
                        }
                      }
                    }

                    .header_wrapper_profile_search {
                      .header_input_search {
                        margin: 0 0.5rem;
                        height: 30px;

                        input {
                          border-radius: 3px;
                          height: 100%;
                          box-shadow: none;
                        }
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
  }
}
</style>
