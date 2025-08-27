<script setup>
import axios from 'axios'
import { useUserStore } from '@/stores/user'
const userStore = useUserStore()
userStore.initStore()
</script>

<template>
  <div class="wrapper_profile w-full">
    <div class="container mx-auto">
      <div class="inner_profile px-2">
        <!-- Sidebar -->
        <aside class="sidebar_profile flex-none" :class="{ sidebar_open: sidebar_open }">
          <!-- Toggle Aside View -->
          <div class="aside_toggle" @click="toggleSidebarOpen">
            <i class="pi pi-angle-double-right"></i>
          </div>
          <!-- Get User Info Of User By Id -->
          <div
            class="user_image"
            @click="activeTab = '1'"
            :class="[activeTab === '1' ? 'activeView' : '']"
          >
            <div class="user_image_icon">
              <i class="pi pi-user"></i>
            </div>
            <div class="user_name_data">
              <div class="">{{ userStore.user.name }}</div>
              <div class="">{{ userStore.user.surname }}</div>
            </div>
          </div>
          <!-- Password Edit If User Is Owner-->
          <div
            class="user_name"
            @click="activeTab = '2'"
            :class="[activeTab === '2' ? 'activeView' : '']"
            v-if="userStore.user.id == user.id"
          >
            <div class="user_name_icon">
              <i class="pi pi-key"></i>
            </div>
            <div class="user_name_data">
              <div class="">******</div>
            </div>
          </div>
          <!-- Get All Friends Of User By Id [Accepted] -->
          <div
            class="user_email"
            @click="activeTab = '3'"
            :class="[activeTab === '3' ? 'activeView' : '']"
          >
            <div class="user_email_icon">
              <fa :icon="['fas', 'users']" class="text-2xl" />
            </div>
            <div class="user_email_data">
              <div class="">Friends All {{ friendsAccepted.length }}</div>
            </div>
          </div>
          <!-- Get All Friends To User Is Suggest [NotSend] -->
          <div
            class="user_Password"
            @click="activeTab = '4'"
            :class="[activeTab === '4' ? 'activeView' : '']"
          >
            <div class="user_Password_icon">
              <fa :icon="['fas', 'user-check']" class="text-2xl" />
            </div>
            <div class="user_Password_data">
              <div class="">Friends Suggest</div>
            </div>
          </div>
          <!-- Get All Friends To User Is Suggest [Waiting] -->
          <div
            class="user_Password"
            @click="activeTab = '5'"
            :class="[activeTab === '5' ? 'activeView' : '']"
            v-if="userStore.user.id == user.id"
          >
            <div class="user_Password_icon">
              <fa :icon="['fas', 'user-plus']" class="text-2xl" />
            </div>
            <div class="user_Password_data">
              <div class="">Friends Requests</div>
            </div>
          </div>
          <!-- Get All Friends User Is  [Send] -->
          <div
            class="user_Password"
            @click="activeTab = '6'"
            :class="[activeTab === '6' ? 'activeView' : '']"
            v-if="userStore.user.id == user.id"
          >
            <div class="user_Password_icon">
              <fa :icon="['fas', 'home']" class="text-2xl" />
            </div>
            <div class="user_Password_data">
              <div class="">User Tasks</div>
            </div>
          </div>
          <!-- User Tasks -->
          <div
            class="user_Password"
            @click="activeTab = '7'"
            :class="[activeTab === '7' ? 'activeView' : '']"
          >
            <div class="user_Password_icon">
              <fa :icon="['fas', 'thumbtack']" class="text-2xl" />
            </div>
            <div class="user_Password_data">
              <div class="">User Tasks</div>
            </div>
          </div>
        </aside>
        <!-- Profile Content -->
        <div class="data_profile flex p-8">
          <!-- User Info -->
          <div
            class="wrapper_info_data w-full mobile_grid_12 tablet_grid_12 laptop_grid_12 laptop_lg_grid_12 desktop_grid_12 desktop_lg_grid_12 gap_20"
            v-if="activeTab === '1'"
          >
            <!-- User Info -->
            <div
              class="mobile_item_12 tablet_item_12 laptop_item_6 laptop_lg_item_6 desktop_item_6 desktop_lg_item_6"
            >
              <div class="wrapper_old_data w-full">
                <div class="inner_old_data w-full">
                  <prime_card class="w-full">
                    <template #header>
                      <!-- Owner Image -->
                      <div class="" v-if="userStore.user.id == user.id">
                        <!-- cover -->
                        <div class="image_cover">
                          <img
                            class="w-full h-64"
                            v-if="userStore.user.get_cover !== 'undefined'"
                            :src="userStore.user.get_cover"
                          />
                          <img
                            class="w-full h-64"
                            v-else-if="userStore.user.get_cover !== ' '"
                            :src="userStore.user.get_cover"
                          />
                          <img
                            class="w-full h-64"
                            v-else
                            src="../../assets/Images/Page_Not_Found/404.jpg"
                          />
                          <img />
                        </div>
                        <!-- Avatar -->
                        <div
                          class="image_avatar border rounded-full"
                          v-if="userStore.user.id == user.id"
                          style="
                            width: 75px;
                            height: 75px;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            margin-top: -37px;
                            margin-left: 10px;
                            position: relative;
                          "
                        >
                          <img
                            class="w-full h-full shadow-lg rounded-full"
                            v-if="userStore.user.get_avatar !== 'undefined'"
                            :src="userStore.user.get_avatar"
                          />
                          <img
                            class="w-full h-full shadow-lg rounded-full"
                            v-else-if="userStore.user.get_avatar == ' '"
                            :src="userStore.user.get_avatar"
                          />
                          <img
                            class="w-full h-full shadow-lg rounded-full"
                            v-else
                            src="../../assets/Images/Page_Not_Found/404.jpg"
                          />
                          <prime_badge
                            size="small"
                            :severity="user.is_online ? 'success' : 'danger'"
                            style="position: absolute; bottom: -8px; opacity: 0.8"
                          ></prime_badge>
                        </div>
                      </div>
                      <!-- User Visit Profile User -->
                      <div v-else class="image_avatar">
                        <!-- Cover -->
                        <div class="image_cover">
                          <img
                            v-if="user.get_cover !== 'https://picsum.photos/200/200'"
                            class="w-full h-64"
                            :src="user.get_cover"
                          />
                          <img
                            class="w-full h-64"
                            v-else
                            src="../../assets/Images/Page_Not_Found/404.jpg"
                          />
                        </div>
                        <!-- Avatar -->
                        <div
                          class="image_avatar border rounded-full"
                          style="
                            width: 75px;
                            height: 75px;
                            display: flex;
                            justify-content: center;
                            align-items: center;
                            margin-top: -37px;
                            margin-left: 10px;
                            position: relative;
                          "
                        >
                          <img
                            class="w-full h-full shadow-lg rounded-full"
                            :src="user.get_avatar"
                            v-if="user.get_avatar !== 'https://picsum.photos/200/200'"
                          />
                          <img
                            class="w-full h-full shadow-lg rounded-full"
                            src="../../assets/Images/Page_Not_Found/404.jpg"
                            v-else
                          />
                          <prime_badge
                            size="small"
                            :severity="user.is_online ? 'success' : 'danger'"
                            style="position: absolute; bottom: -8px; opacity: 0.8"
                          ></prime_badge>
                        </div>
                      </div>
                    </template>
                    <!-- name Surname Email-->
                    <template #content>
                      <div
                        class="w-full mobile_grid_12 tablet_grid_12 laptop_grid_12 laptop_lg_grid_12 desktop_grid_12 desktop_lg_grid_12"
                      >
                        <div
                          class="mobile_item_12 tablet_item_12 laptop_item_6 laptop_lg_item_6 desktop_item_6 desktop_lg_item_6 mr-1"
                        >
                          <!-- name -->
                          <div class="">
                            <h3 class="text-2xl font-bold" v-if="userStore.user.id == user.id">
                              {{ formInfo.name }}
                            </h3>
                            <h3 class="text-2xl font-bold" v-else>{{ user.name }}</h3>
                          </div>
                          <!-- Surname -->
                          <div class="">
                            <h3 class="text-1xl font-bold" v-if="userStore.user.id == user.id">
                              {{ formInfo.surname }}
                            </h3>
                            <h3 class="text-1xl font-bold" v-else>
                              {{ user.surname }}
                            </h3>
                          </div>
                          <!-- Email -->
                          <div class="">
                            <small class="text-1xl font-bold" v-if="userStore.user.id == user.id">
                              {{ formInfo.email }}
                            </small>
                            <small class="text-1xl font-bold" v-else>
                              {{ user.email }}
                            </small>
                          </div>
                          <div class="flex justify-between items-center">
                            <!-- date of birth -->
                            <div class="mr-4">
                              <h3 class="text-1xl font-bold" v-if="userStore.user.id == user.id">
                                {{ formInfo.date_of_birth }}
                              </h3>
                              <h3 class="text-1xl font-bold" v-else>
                                {{ user.date_of_birth }}
                              </h3>
                            </div>
                            <!-- gender -->
                            <div class="mr-4">
                              <h3 class="text-1xl font-bold" v-if="userStore.user.id == user.id">
                                {{ formInfo.gender }}
                              </h3>
                              <h3 class="text-1xl font-bold" v-else>
                                {{ user.gender }}
                              </h3>
                            </div>
                          </div>
                        </div>
                        <div
                          class="mobile_item_12 tablet_item_12 laptop_item_6 laptop_lg_item_6 desktop_item_6 desktop_lg_item_6 ml-1"
                        >
                          <!-- date of birth   gender skills -->
                          <div class="flex justify-between items-center my-2">
                            <!-- skills -->
                            <div class="">
                              <div class="" v-if="userStore.user.id == user.id">
                                <prime_tag
                                  severity="success"
                                  v-for="skill in formInfo.skills"
                                  :key="skill"
                                  class="mb-1 ml-1"
                                >
                                  <span>
                                    <prime_tag severity="success" :value="skill"> </prime_tag>
                                  </span>
                                </prime_tag>
                              </div>
                              <div class="" v-else>
                                <prime_tag
                                  severity="success"
                                  v-for="skill in user.skills"
                                  :key="skill"
                                  class="mb-1 ml-1"
                                >
                                  <span>
                                    <prime_tag severity="success" :value="skill"> </prime_tag>
                                  </span>
                                </prime_tag>
                              </div>
                            </div>
                          </div>
                        </div>
                      </div>
                    </template>
                    <!-- Count [Friends , آخر تسجيل دخول ] -->
                    <template #footer>
                      <!-- Friends  Tasks -->
                      <div class="flex justify-between items-center py-1">
                        <div class="">
                          <prime_button
                            type="button"
                            label="Friends"
                            :badge="user.friends_count"
                            badgeSeverity="contrast"
                            outlined
                          />
                        </div>
                        <div class="">
                          <prime_button
                            type="button"
                            label="Tasks"
                            :badge="user.task_count"
                            badgeSeverity="contrast"
                            outlined
                          />
                        </div>
                        <!-- آخر تسجيل دخول -->
                        <div class="flex justify-between item-center py-1">
                          <small>Last Login: {{ user.last_login_formatted }} Ago </small>
                        </div>
                      </div>
                      <!-- اذا كان زائر  -->
                      <!-- ارسال طلب صداقة -->
                      <div class="">
                        <div class="flex justify-between py-2">
                          <!-- ارسال طلب صداقة -->
                          <prime_button
                            @click="sendFriendshipRequest"
                            class="border py-2 px-4 btn-primary Add_friend"
                            v-if="can_send_friendship_request"
                          >
                            <span class="icon">
                              <fa :icon="['fas', 'plus']"></fa>
                            </span>
                            <span class="text"> Add Friend</span>
                          </prime_button>
                          <!-- زر إلغاء طلب الصداقة -->
                          <div v-else>
                            <!-- Click To Un Friend -->
                            <prime_button
                              class="mr-1 un_friend"
                              v-if="(userStore.user.id != user.id) & (isFriendsAccepted == true)"
                              @click="handleRequest('unfriend', user.id)"
                            >
                              <span class="icon">
                                <fa :icon="['fas', 'user']"></fa>
                              </span>
                              <span class="text"> Un Friend </span>
                            </prime_button>
                            <prime_button
                              class="friend"
                              v-if="(userStore.user.id != user.id) & (isFriendsAccepted == true)"
                            >
                              <span class="icon">
                                <fa :icon="['fas', 'user']"></fa>
                              </span>
                              <span class="text"> Friend </span>
                            </prime_button>
                            <!-- Click To [Accepted] -->
                            <prime_button
                              class="btn btn-primary Add_friend"
                              v-if="(userStore.user.id != user.id) & (isFriendsSend == true)"
                              @click="handleRequest('accepted', user.id)"
                            >
                              <span class="icon">
                                <fa :icon="['fas', 'user-check']"></fa>
                              </span>
                              <span class="text"> accepted </span>
                            </prime_button>
                            <!-- Click To [Rejected] -->
                            <prime_button
                              class="btn btn-primary Add_friend"
                              v-if="(userStore.user.id != user.id) & (isFriendsSend == true)"
                              @click="handleRequest('rejected', user.id)"
                            >
                              <span class="icon">
                                <fa :icon="['fas', 'user-check']"></fa>
                              </span>
                              <span class="text"> rejected </span>
                            </prime_button>
                            <!-- Click To Cancel [Waiting] -->
                            <prime_button
                              class="btn btn-primary Add_friend"
                              v-if="(userStore.user.id != user.id) & (isFriendsWaiting == true)"
                              @click="handleRequest('cancel', user.id)"
                            >
                              <span class="icon">
                                <fa :icon="['fas', 'user-check']"></fa>
                              </span>
                              <span class="text"> Cancel Request </span>
                            </prime_button>
                          </div>
                          <!-- ارسال رساله -->
                          <prime_button
                            class="message_friend"
                            @click="sendDirectMessage"
                            v-if="userStore.user.id != user.id"
                          >
                            <span class="icon">
                              <fa :icon="['fab', 'facebook-messenger']"></fa>
                            </span>
                            <span class="text"> Message</span>
                          </prime_button>
                        </div>
                      </div>
                    </template>
                  </prime_card>
                </div>
              </div>
            </div>
            <!-- Is Owner Send Data -->
            <div
              class="mobile_item_12 tablet_item_12 laptop_item_6 laptop_lg_item_6 desktop_item_6 desktop_lg_item_6"
            >
              <div class="wrapper_new_data" v-if="userStore.user.id == user.id">
                <form class="space-y-4" v-on:submit.prevent="formEditProfileInfo">
                  <!-- Avatar -->
                  <!-- Cover -->
                  <div
                    class="w-full mobile_grid_12 tablet_grid_12 laptop_grid_12 laptop_lg_grid_12 desktop_grid_12 desktop_lg_grid_12 gap_10"
                  >
                    <!--  Avatar  -->
                    <div
                      class="new_data mobile_item_12 tablet_item_12 laptop_item_12 laptop_lg_item_12 desktop_item_6 desktop_lg_item_6"
                    >
                      <label for="websiteImage" class="font-semibold block my-2">Avatar</label>
                      <prime_file_upload
                        type="file"
                        ref="fileAvatar"
                        :multiple="true"
                        name="demo[]"
                        @select="handleAvatarFileUpload"
                        accept="image/*"
                        :maxFileSize="1000000"
                      >
                        <template #empty>
                          <span>Drag and drop files to here to upload.</span>
                        </template>
                      </prime_file_upload>
                    </div>
                    <!-- Cover -->
                    <div
                      class="new_data mobile_item_12 tablet_item_12 laptop_item_12 laptop_lg_item_12 desktop_item_6 desktop_lg_item_6"
                    >
                      <label for="websiteImage" class="font-semibold block my-2">Cover</label>
                      <prime_file_upload
                        type="file"
                        ref="fileCover"
                        :multiple="true"
                        name="demo[]"
                        @select="handleCoverFileUpload"
                        accept="image/*"
                        :maxFileSize="1000000"
                      >
                        <template #empty>
                          <span>Drag and drop files to here to upload.</span>
                        </template>
                      </prime_file_upload>
                    </div>
                  </div>
                  <!-- Name Surname -->
                  <div class="flex justify-between items-center">
                    <!-- Name -->
                    <div class="new_data">
                      <label>Name</label><br />
                      <input
                        type="text"
                        v-model="formInfo.name"
                        placeholder="Your full name"
                        class="w-full mt-2 py-2 px-4 border border-gray-200 rounded-lg"
                      />
                    </div>
                    <!-- Surname -->
                    <div class="new_data">
                      <label>Surname</label><br />
                      <input
                        type="text"
                        v-model="formInfo.surname"
                        placeholder="Your full Surname"
                        class="w-full mt-2 py-2 px-4 border border-gray-200 rounded-lg"
                      />
                    </div>
                  </div>
                  <!-- Email -->
                  <div class="new_data">
                    <label>E-mail</label><br />
                    <input
                      type="email"
                      v-model="formInfo.email"
                      placeholder="Your e-mail address"
                      class="w-full mt-2 py-2 px-4 border border-gray-200 rounded-lg"
                    />
                  </div>
                  <!-- Skills -->
                  <div class="new_data">
                    <label>Skills [press alt + comma to add]:</label><br />
                    <input
                      type="text"
                      v-model="tempSkill"
                      @keyup.alt="addSkill"
                      placeholder="Your Skills"
                      class="w-full mt-2 py-2 px-4 border border-gray-200 rounded-lg"
                    />
                    <div class="grid_12 mt-4">
                      <div class="">
                        <span @click="deleteSkill(skill)" class="cursor-pointer">
                          <prime_tag
                            severity="success"
                            v-for="skill in formInfo.skills"
                            :key="skill"
                            class="mr-1"
                          >
                            <span @click="deleteSkill(skill)" class="item_1">
                              <prime_tag severity="success" :value="skill"> </prime_tag>
                            </span>
                          </prime_tag>
                        </span>
                      </div>
                    </div>
                  </div>
                  <!-- Date of birth -->
                  <div class="col-span-full">Date of birth</div>
                  <div class="col-span-full">
                    <div class="flex flex-col md:flex-row gap-2">
                      <!-- Day -->
                      <prime_input_group>
                        <prime_date_picker v-model="day" view="day" dateFormat="dd" />
                      </prime_input_group>
                      <!-- Month -->
                      <prime_input_group>
                        <prime_date_picker v-model="month" view="month" dateFormat="mm" />
                      </prime_input_group>
                      <!-- Year -->
                      <prime_input_group>
                        <prime_date_picker v-model="year" view="year" dateFormat="yy" />
                      </prime_input_group>
                    </div>
                  </div>
                  <!-- Gender -->
                  <div class="col-span-full">Gender</div>
                  <div class="flex flex-col md:flex-row gap-2">
                    <prime_input_group>
                      <prime_radio_button
                        v-model="formInfo.gender"
                        inputId="ingredient1"
                        name="gender"
                        value="Female"
                      />
                      <label for="ingredient1" class="ml-2"> Female </label>
                    </prime_input_group>
                    <prime_input_group>
                      <prime_radio_button
                        v-model="formInfo.gender"
                        inputId="ingredient2"
                        name="gender"
                        value="Male"
                      />
                      <label for="ingredient2" class="ml-2"> Male </label>
                    </prime_input_group>
                    <prime_input_group>
                      <prime_radio_button
                        v-model="formInfo.gender"
                        inputId="ingredient3"
                        name="gender"
                        value="Custom"
                      />
                      <label for="ingredient3" class="ml-2"> Custom </label>
                    </prime_input_group>
                  </div>
                  <!-- Is Online -->
                  <div class="new_data">
                    <label class="col-span-full">Is Online</label><br />
                    <input type="checkbox" v-model="formInfo.is_online" />
                    <label class="col-span-full">{{ formInfo.is_online }}</label>
                  </div>
                  <!-- Click Send -->
                  <div>
                    <button
                      class="py-4 px-6 bg-blue-400 text-white rounded-lg"
                      v-on:click.prevent="formEditProfileInfo"
                    >
                      Save changes
                    </button>
                  </div>
                </form>
              </div>
            </div>
          </div>
          <!-- wrapper_password_data -->
          <div
            class="wrapper_password_data flex justify-between items-center"
            v-if="activeTab === '2'"
          >
            <div class="wrapper_old_data">
              <div class="inner_old_data flex justify-between items-end">
                <prime_card class="w-96">
                  <template #header>
                    <img
                      v-if="userStore.user.get_avatar != 'undefined'"
                      :src="userStore.user.get_avatar"
                    />
                    <img v-else src="../../assets/Images/Page_Not_Found/404.jpg" />
                    <img />
                  </template>
                  <template #content>
                    <h3 class="text-2xl font-bold">
                      {{ userStore.user.name }}
                    </h3>
                    <h3 class="text-1xl font-bold">
                      {{ userStore.user.surname }}
                    </h3>
                  </template>
                  <template #body>
                    <div class="">{{ userStore.user.email }}</div>
                  </template>
                  <template #footer>{{ userStore.user.email }}</template>
                </prime_card>
              </div>
            </div>
            <div class="wrapper_new_data ml-8" v-if="userStore.user.id == user.id">
              <form class="space-y-6" v-on:submit.prevent="submitForm">
                <div class="new_data">
                  <label>Old password</label><br />
                  <input
                    type="password"
                    v-model="formPassword.old_password"
                    placeholder="Your old password"
                    class="w-full mt-2 py-2 px-4 border border-gray-200 rounded-lg"
                  />
                </div>

                <div class="new_data">
                  <label>New password</label><br />
                  <input
                    type="password"
                    v-model="formPassword.new_password1"
                    placeholder="Your new password"
                    class="w-full mt-2 py-2 px-4 border border-gray-200 rounded-lg"
                  />
                </div>

                <div class="new_data">
                  <label>Repeat password</label><br />
                  <input
                    type="password"
                    v-model="formPassword.new_password2"
                    placeholder="Repeat password"
                    class="w-full mt-2 py-2 px-4 border border-gray-200 rounded-lg"
                  />
                </div>
                <div>
                  <button class="py-4 px-6 bg-blue-400 text-white rounded-lg">Save changes</button>
                </div>
              </form>
            </div>
          </div>
          <!-- Get All Friends Of User By Id [Accepted]  -->
          <div class="w-full" v-if="activeTab === '3'">
            <div class="main-center col-span-2 space-y-4">
              <!-- Header -->
              <div class="flex justify-between items-center mb-6">
                <h3 class="text-3xl">Your Friends</h3>
                <prime_button
                  type="button"
                  label="All Friends"
                  icon="pi pi-user-plus"
                  :badge="allFriends.length"
                  badgeSeverity="contrast"
                  outlined
                />
              </div>
              <!-- Main -->
              <div
                class="w-full mobile_grid_12 tablet_grid_12 laptop_grid_12 laptop_lg_grid_12 desktop_grid_12 desktop_lg_grid_12"
                v-if="allFriends.length"
              >
                <!-- Start Card -->
                <prime_card
                  v-if="allFriends.length"
                  style="overflow: hidden; position: relative"
                  v-for="user in allFriends"
                  v-bind:key="user.id"
                  class="mobile_item_12 tablet_item_12 laptop_item_6 laptop_lg_item_2 desktop_item_3 desktop_lg_item_3 m-2"
                >
                  <template #header>
                    <img
                      alt="user header"
                      :src="user.get_cover"
                      class="h-32 md:h-20 lg:h-32 w-full m-auto"
                    />
                    <div style="position: relative">
                      <img
                        :src="user.get_avatar"
                        class="mb-1 rounded-full h-14 md:h-10 w-14 md:w-10 m-auto"
                        style="margin-top: -7px; position: absolute; top: -15px; left: 10px"
                      />
                    </div>
                  </template>
                  <template #title>
                    <p class="mt-1 md:mt-1">
                      <strong @click="activeTab = '1'">
                        <RouterLink :to="{ name: 'profile', params: { id: user.id } }">{{
                          user.name
                        }}</RouterLink>
                      </strong>
                    </p>
                  </template>
                  <template #subtitle>Card subtitle</template>
                  <template #content> </template>
                  <template #footer>
                    <div
                      class="w-full mobile_grid_12 tablet_grid_12 laptop_grid_12 laptop_lg_grid_12 desktop_grid_12 desktop_lg_grid_12"
                    >
                      <div
                        class="mobile_item_3 tablet_item_3 laptop_item_3 laptop_lg_item_3 desktop_item_3 desktop_lg_item_3"
                      >
                        <prime_button
                          :label="'Friends ' + user.friends_count"
                          severity="secondary"
                          outlined
                          class="w-full"
                        />
                      </div>
                      <div
                        class="mobile_item_9 tablet_item_9 laptop_item_9 laptop_lg_item_9 desktop_item_9 desktop_lg_item_9"
                      >
                        <prime_button :label="user.email" class="w-full" />
                      </div>
                    </div>
                  </template>
                </prime_card>
                <!-- End Card -->
                <!-- Start Card -->
                <prime_card
                  v-else
                  style="overflow: hidden; position: relative"
                  v-for="user in friendsAccepted"
                  v-bind:key="user.id"
                  class="mobile_item_12 tablet_item_12 laptop_item_6 laptop_lg_item_2 desktop_item_3 desktop_lg_item_3 m-2"
                >
                  <template #header>
                    <img
                      alt="user header"
                      :src="user.get_cover"
                      class="h-32 md:h-20 lg:h-32 w-full m-auto"
                    />
                    <div style="position: relative">
                      <img
                        :src="user.get_avatar"
                        class="mb-1 rounded-full h-14 md:h-10 w-14 md:w-10 m-auto"
                        style="margin-top: -7px; position: absolute; top: -15px; left: 10px"
                      />
                    </div>
                  </template>
                  <template #title>
                    <p class="mt-1 md:mt-1">
                      <strong @click="activeTab = '1'">
                        <RouterLink :to="{ name: 'profile', params: { id: user.id } }">{{
                          user.name
                        }}</RouterLink>
                      </strong>
                    </p>
                  </template>
                  <template #subtitle>Card subtitle</template>
                  <template #content> </template>
                  <template #footer>
                    <div
                      class="w-full mobile_grid_12 tablet_grid_12 laptop_grid_12 laptop_lg_grid_12 desktop_grid_12 desktop_lg_grid_12"
                    >
                      <div
                        class="mobile_item_3 tablet_item_3 laptop_item_3 laptop_lg_item_3 desktop_item_3 desktop_lg_item_3"
                      >
                        <prime_button
                          :label="'Friends ' + user.friends_count"
                          severity="secondary"
                          outlined
                          class="w-full"
                        />
                      </div>
                      <div
                        class="mobile_item_9 tablet_item_9 laptop_item_9 laptop_lg_item_9 desktop_item_9 desktop_lg_item_9"
                      >
                        <prime_button :label="user.email" class="w-full" />
                      </div>
                    </div>
                  </template>
                </prime_card>
                <!-- End Card -->
              </div>
            </div>
          </div>
          <!-- Get All Friends To User Is Suggest [NotSend] -->
          <div class="w-full" v-if="activeTab === '4'">
            <!-- Header -->
            <div class="flex justify-between items-center mb-6">
              <h3 class="text-xl">People You May Know [ Suggest ]</h3>
              <prime_button
                type="button"
                label="Friendship Not Send "
                icon="pi pi-user-plus"
                :badge="friendsNotSend.length"
                badgeSeverity="contrast"
                outlined
              />
            </div>
            <!-- Content -->
            <div
              class="w-full mobile_grid_12 tablet_grid_12 laptop_grid_12 laptop_lg_grid_12 desktop_grid_12 desktop_lg_grid_12"
            >
              <!-- Start Card -->
              <prime_card
                style="overflow: hidden; position: relative"
                v-for="user in friendsNotSend"
                v-bind:key="user.id"
                class="mobile_item_12 tablet_item_12 laptop_item_6 laptop_lg_item_3 desktop_item_3 desktop_lg_item_2 mx-2 mb-4"
              >
                <template #header>
                  <img
                    alt="user header"
                    :src="user.get_cover"
                    class="h-32 md:h-20 lg:h-32 w-full m-auto"
                    v-if="user.get_avatar !== 'https://picsum.photos/200/200'"
                  />
                  <img
                    src="../../assets/Images/Page_Not_Found/404.jpg"
                    class="h-32 md:h-20 lg:h-32 w-full m-auto"
                    v-else
                  />
                  <div style="position: relative">
                    <img
                      :src="user.get_avatar"
                      class="mb-1 rounded-full h-14 md:h-10 w-14 md:w-10 m-auto"
                      style="margin-top: -7px; position: absolute; top: -15px; left: 10px"
                      v-if="user.get_avatar != 'https://picsum.photos/200/200'"
                    />
                    <img
                      src="../../assets/Images/Page_Not_Found//404.jpg"
                      class="mb-1 rounded-full h-14 md:h-10 w-14 md:w-10 m-auto"
                      style="margin-top: -7px; position: absolute; top: -15px; left: 10px"
                      v-else
                    />
                  </div>
                </template>
                <template #title>
                  <p class="mt-4 md:mt-4">
                    <strong @click="activeTab = '1'">
                      <RouterLink :to="{ name: 'profile', params: { id: user.id } }">
                        <span v-if="user.name">{{ user.name }}</span>
                        <span v-else>User Name</span>
                      </RouterLink>
                    </strong>
                  </p>
                </template>
                <template #subtitle>{{ user.email }}</template>
                <template #content>
                  <!-- ارسال طلب صداقة -->
                  <prime_button
                    @click="sendFriendshipRequestById(user.id)"
                    class="border py-2 px-4 btn-primary Add_friend"
                    v-if="can_send_friendship_request"
                  >
                    <span class="icon">
                      <fa :icon="['fas', 'plus']"></fa>
                    </span>
                    <span class="text"> Add Friend</span>
                  </prime_button>
                </template>
                <template #footer>
                  <div class="flex gap-4 mt-1">
                    <prime_button
                      :label="'Friends ' + user.friends_count"
                      severity="secondary"
                      outlined
                      class="w-full"
                    />
                  </div>
                </template>
              </prime_card>
              <!-- End Card -->
            </div>
          </div>
          <!-- Get All Friends For User Is Waiting [Waiting] -->
          <div class="w-full" v-if="activeTab === '5'">
            <!-- friends Waiting -->
            <div class="w-full" v-if="friendsWaiting.length">
              <!-- Header -->
              <div class="flex justify-between items-center mb-6">
                <h3 class="text-xl">Friendship Requests Waiting</h3>
                <prime_button
                  type="button"
                  label="Friendship Requests Waiting"
                  icon="pi pi-user-plus"
                  :badge="friendsWaiting.length"
                  badgeSeverity="contrast"
                  outlined
                />
              </div>
              <!-- Content -->
              <div class="rounded-lg grid grid-cols-3 gap-4 mt-3">
                <div
                  class="text-center border shadow-xl rounded-lg p-4"
                  v-for="friendWaiting in friendsWaiting"
                  v-bind:key="friendWaiting.id"
                >
                  <img :src="friendWaiting.get_avatar" class="mb-6 rounded-full h-32 w-32 m-auto" />
                  <p @click="activeTab = '1'">
                    <strong>
                      <RouterLink
                        :to="{
                          name: 'profile',
                          params: { id: friendWaiting.id },
                        }"
                        >{{ friendWaiting.name }}</RouterLink
                      >
                    </strong>
                  </p>

                  <div class="mt-6 flex space-x-8 justify-around">
                    <p class="text-xs text-gray-500">{{ friendWaiting.friends_count }} Friends</p>
                    <p class="text-xs text-gray-500">{{ friendWaiting.posts_count }} Tasks</p>
                  </div>

                  <div class="mt-4 flex justify-between">
                    <button
                      class="inline-block py-2 px-4 bg-blue-400 text-white rounded-lg"
                      @click="handleRequest('accepted', friendWaiting.id)"
                    >
                      Accept
                    </button>
                    <button
                      class="inline-block py-2 px-4 bg-red-600 text-white rounded-lg"
                      @click="handleRequest('rejected', friendWaiting.id)"
                    >
                      Reject
                    </button>
                  </div>
                </div>
              </div>
            </div>
            <div class="w-full" v-else>
              <div class="flex justify-between items-center mb-6">
                <h3 class="text-xl">No Friendship Requests</h3>
                <prime_button
                  type="button"
                  label="Friendship requests"
                  icon="pi pi-user-plus"
                  :badge="friendsWaiting.length"
                  badgeSeverity="contrast"
                  outlined
                />
              </div>
            </div>
          </div>
          <!-- Get All Friends  User Is  [Send] -->
          <div class="w-full" v-if="activeTab === '6'">
            <!-- Header -->
            <div class="flex justify-between items-center mb-6">
              <h3 class="text-xl uppercase">User Is [Send]</h3>
              <prime_button
                type="button"
                label="User Is  [Send]"
                icon="pi pi-user-plus"
                :badge="friendsSuggest.length"
                badgeSeverity="contrast"
                outlined
              />
            </div>
            <div
              class="w-full mobile_grid_12 tablet_grid_12 laptop_grid_12 laptop_lg_grid_12 desktop_grid_12 desktop_lg_grid_12"
            >
              <!-- Start Card -->
              <prime_card
                style="overflow: hidden; position: relative"
                v-for="user in friendsSend"
                v-bind:key="user.id"
                class="mobile_item_12 tablet_item_12 laptop_item_6 laptop_lg_item_2 desktop_item_3 desktop_lg_item_3 mx-2 mb-4"
              >
                <template #header>
                  <img
                    alt="user header"
                    :src="user.get_cover"
                    class="h-32 md:h-20 lg:h-32 w-full m-auto"
                    v-if="user.get_avatar !== 'https://picsum.photos/200/200'"
                  />
                  <img
                    src="../../assets/Images/Page_Not_Found/404.jpg"
                    class="h-32 md:h-20 lg:h-32 w-full m-auto"
                    v-else
                  />
                  <div style="position: relative">
                    <img
                      :src="user.get_avatar"
                      class="mb-1 rounded-full h-14 md:h-10 w-14 md:w-10 m-auto"
                      style="margin-top: -7px; position: absolute; top: -15px; left: 10px"
                      v-if="user.get_avatar != 'https://picsum.photos/200/200'"
                    />
                    <img
                      src="../../assets/Images/Page_Not_Found//404.jpg"
                      class="mb-1 rounded-full h-14 md:h-10 w-14 md:w-10 m-auto"
                      style="margin-top: -7px; position: absolute; top: -15px; left: 10px"
                      v-else
                    />
                  </div>
                </template>
                <template #title>
                  <p class="mt-4 md:mt-4">
                    <strong @click="activeTab = '1'">
                      <RouterLink :to="{ name: 'profile', params: { id: user.id } }">{{
                        user.name
                      }}</RouterLink>
                    </strong>
                  </p>
                </template>
                <template #subtitle>{{ user.email }}</template>
                <template #content> </template>
                <template #footer>
                  <div class="flex gap-4 mt-1">
                    <prime_button
                      :label="'Friends ' + user.friends_count"
                      severity="secondary"
                      outlined
                      class="w-full"
                    />
                  </div>
                </template>
              </prime_card>
              <!-- End Card -->
            </div>
          </div>
          <!-- Get All Of User Tasks -->
          <div class="w-full" v-if="activeTab === '7'">
            <!-- Header -->
            <div class="flex justify-between items-center mb-6">
              <h3 class="text-xl uppercase">Your Tasks</h3>
              <prime_button
                type="button"
                label="All Tasks"
                icon="pi pi-user-plus"
                :badge="friendsSuggest.length"
                badgeSeverity="contrast"
                outlined
              />
            </div>
          </div>
          <!-- Errors -->
          <template v-if="errorsFormInfo.length > 0">
            <div class="bg-red-300 text-white rounded-lg p-6">
              <p v-for="error in errorsFormInfo" v-bind:key="error">
                {{ error }}
              </p>
            </div>
          </template>
          <template v-if="errorsFormPassword.length > 0">
            <div class="bg-red-300 text-white rounded-lg p-6">
              <p v-for="error in errorsFormPassword" v-bind:key="error">
                {{ error }}
              </p>
            </div>
          </template>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// استيراد مكتبة Moment.js
// import moment from 'moment'

export default {
  name: 'profileView',
  setup() {
    return {}
  },
  beforeCreate() {},
  data() {
    return {
      // 🧑 User Info
      user: {
        id: '',
      },
      // Friends
      can_send_friendship_request: null,
      friendship_status: '',
      friendsAccepted: [],
      isFriendsAccepted: false,
      friendsWaiting: [],
      isFriendsWaiting: false,
      friendsRejected: [],
      friendsCancelled: [],
      friendsNotSend: [],
      friendsSend: [],
      isFriendsSend: false,
      allFriends: [],
      friendshipRequests: [],
      friendsSuggest: [],
      // Layer
      sidebar_open: false,
      activeTab: `1`,
      // Form Info
      formInfo: {
        name: ``,
        surname: ``,
        email: ``,
        date_of_birth: ``,
        gender: ``,
        is_online: false,
        skills: [],
      },
      selectedImageAvatarFile: null,
      selectedImageCoverFile: null,
      tempSkill: '',
      day: '',
      month: '',
      year: '',
      errorsFormInfo: [],
      // Form Password
      formPassword: {
        old_password: '',
        new_password1: '',
        new_password2: '',
      },
      errorsFormPassword: [],
      //
    }
  },
  watch: {
    '$route.params.id': {
      handler: function () {
        this.getProfile()
      },
      deep: true,
      immediate: true,
    },
  },
  mounted() {
    document.title = 'Profile'
    this.getFriends()
    this.getFriendSuggestions()
    // التأكد من أن بيانات المستخدم موجودة قبل محاولة الوصول إليها
    // عند تسجيل الدخول localStorage تحميل البيانات من
    const userStore = useUserStore()
    if (userStore.user) {
      this.formInfo.name = userStore.user.name
      this.formInfo.surname = userStore.user.surname
      this.formInfo.email = userStore.user.email
      // this.formInfo.date_of_birth = userStore.user.date_of_birth
      let daySlice = userStore.user.date_of_birth.slice(8, 11)
      this.day = daySlice
      let dayMonth = userStore.user.date_of_birth.slice(5, 7)
      this.month = dayMonth
      let dayYear = userStore.user.date_of_birth.slice(0, 4)
      this.year = dayYear
      this.formInfo.date_of_birth = userStore.user.date_of_birth.slice(0, 11)
      this.formInfo.gender = userStore.user.gender
      this.formInfo.is_online = userStore.user.is_online
      this.formInfo.skills = userStore.user.skills
    }
  },
  methods: {
    // 👇 Toggle Aside View
    toggleSidebarOpen() {
      this.sidebar_open = !this.sidebar_open
    },
    // ____________________________________________
    // ____________________________________________
    // ____________________________________________
    // 🧑 User Info
    // ____________________________________________
    // ____________________________________________
    // ____________________________________________
    // 🧑 Get Profile Info By Id
    getProfile() {
      const userStore = useUserStore()
      axios
        .get(`/api/profile/${this.$route.params.id}/`)
        .then((response) => {
          this.user = response.data.user
          this.can_send_friendship_request = response.data.can_send_friendship_request
          // For Test
          let line = '🧑'.repeat(30)
          console.log(` %c${line} `, 'color: #1cd07c; font-size: 16px')
          console.log('Profile Django Data Of User: ', response.data)
          if (response.data.user.id == userStore.user.id) {
            this.can_send_friendship_request = false
          }
        })
        .catch((error) => {
          console.error('error', error)
          this.$toast.add({
            severity: 'error',
            summary: `Error 🧑 Get Profile Info By Id `,
            detail: `${error.message}`,
            life: 3000,
          })
        })
    },
    addSkill($event) {
      if ($event.key === ',' && this.tempSkill) {
        if (!this.formInfo.skills.includes(this.tempSkill)) {
          this.formInfo.skills.push(this.tempSkill)
        }
        this.tempSkill = ''
      }
    },
    deleteSkill(skill) {
      this.formInfo.skills = this.formInfo.skills.filter((item) => {
        return skill !== item
      })
    },
    // For Upload Avatar Image to Post Store and for Post
    handleAvatarFileUpload(event) {
      // let file = event.target.files[0]
      // يمكن الحصول على الملفات من event.files
      const file = event.files ? event.files[0] : null
      if (file) {
        console.log('file: ', file)
        this.selectedImageAvatarFile = file
        console.log('FormData contains image:', this.selectedImageAvatarFile.name)
        // Send Image to View
        this.$toast.add({
          severity: 'success',
          summary: `Data contains image`,
          detail: `${this.selectedImageAvatarFile.name}`,
          life: 3000,
        })
      } else {
        console.log('No file selected.')
      }
    },
    // For Upload Avatar Image to Post Store and for Post
    handleCoverFileUpload(event) {
      // let file = event.target.files[0]
      // يمكن الحصول على الملفات من event.files
      const file = event.files ? event.files[0] : null
      if (file) {
        console.log('file: ', file)
        this.selectedImageCoverFile = file
        console.log('FormData contains image:', this.selectedImageCoverFile.name)
        // Send Image to View
        this.$toast.add({
          severity: 'success',
          summary: `Data contains image`,
          detail: `${this.selectedImageCoverFile.name}`,
          life: 3000,
        })
      } else {
        console.log('No file selected.')
      }
    },
    // 📝 Update User Profile Info
    formEditProfileInfo() {
      this.errorsFormInfo = []
      const userStore = useUserStore()

      if (this.errorsFormInfo.length === 0) {
        // التحقق من وجود بيانات المستخدم في المتجر
        if (userStore && userStore.user) {
          // استخراج اليوم، الشهر، والسنة من كائنات Date وتنسيقها
          const day = this.day
          const month = this.month
          const year = this.year
          const formattedDate = `${year}-${month}-${day}`
          // إعداد البيانات المرسلة مع الطلب
          let formData = new FormData()
          // Add Image [ Avatar ] إضافة الصور إذا تم تحديدها
          if (this.selectedImageAvatarFile) {
            // formData.append('avatar', this.$refs.fileAvatar.files[0])
            formData.append('avatar', this.selectedImageAvatarFile)
          }
          // Add Image [ Cover ] إضافة الصور إذا تم تحديدها
          if (this.selectedImageCoverFile) {
            // formData.append('cover', this.$refs.fileCover.files[0])
            formData.append('cover', this.selectedImageCoverFile)
          }
          formData.append('name', this.formInfo.name)
          formData.append('surname', this.formInfo.surname)
          formData.append('email', this.formInfo.email)
          formData.append('date_of_birth', formattedDate)
          formData.append('gender', this.formInfo.gender)
          formData.append('is_online', this.formInfo.is_online)
          formData.append('skills', JSON.stringify(this.formInfo.skills))

          axios
            .post('/api/editprofile/', formData, {
              headers: {
                'Content-Type': 'multipart/form-data',
              },
            })
            .then((response) => {
              // localStorage تحديث البيانات في
              // قم بتحديث معلومات المستخدم في المتجر
              userStore.setUserInfo({
                id: userStore.user.id,
                name: this.formInfo.name,
                surname: this.formInfo.surname,
                email: this.formInfo.email,
                date_of_birth: response.data.user.date_of_birth,
                gender: this.formInfo.gender,
                get_avatar: response.data.user.get_avatar,
                get_cover: response.data.user.get_cover,
                is_online: response.data.user.is_online,
                skills: response.data.user.skills,
              })
              if (response.data.message === 'information updated') {
                this.$toast.add({
                  severity: 'success',
                  summary: `🧑 Profile`,
                  detail: `The information was saved`,
                  life: 3000,
                })
                console.log('response: ', response)
                console.log('response Send To Django: ', response.data)
              }
            })
            .catch((error) => {
              console.log('error', error)
            })
        }
      }
    },
    // ____________________________________________
    // ____________________________________________
    // ____________________________________________
    // 🧑 Get All Friends
    // ____________________________________________
    // ____________________________________________
    // ____________________________________________
    // 🧑 Get All Friends
    async getFriends() {
      await axios
        .get(`/api/friends/${this.$route.params.id}/`)
        .then((response) => {
          this.getProfile()
          const userStore = useUserStore()
          // 📝 Debugging Output
          let line = '📌'.repeat(30)
          console.log(`%c${line}`, 'color: #1cd07c; font-size: 16px')
          console.log('Friends All Data:', response.data)

          // Storing all friends data in one object
          this.friendsData = response.data.friends

          // Extracting individual friend categories (if needed)
          this.friendsAccepted = this.friendsData.accepted
          for (let index = 0; index < this.friendsAccepted.length; index++) {
            const element = this.friendsAccepted[index]
            if (userStore.user.id == element.id) {
              this.isFriendsAccepted = true
            } else {
              this.isFriendsAccepted = false
            }
          }
          this.allFriends = this.friendsData.all
          // console.log('this.allFriends: ', this.allFriends)
          for (let index = 0; index < this.allFriends.length; index++) {
            const element = this.allFriends[index]
            // console.log('element.id: ', element.id)
            // console.log('userStore.user.id: ', userStore.user.id)
            this.user = response.data.user
            this.can_send_friendship_request = response.data.can_send_friendship_request
            // For Test
            // let line = '📌'.repeat(30)
            // console.log(` %c${line} `, 'color: #1cd07c; font-size: 16px')
            // console.log('Profile Django Data Of User: ', response.data)
            // if (response.data.user.id == userStore.user.id) {
            // }
            if (userStore.user.id == element.id) {
              this.isFriendsAccepted = true
              this.can_send_friendship_request = false
            } else {
              this.can_send_friendship_request = true
              this.isFriendsAccepted = false
            }
          }
          this.friendsWaiting = this.friendsData.waiting
          for (let index = 0; index < this.friendsWaiting.length; index++) {
            const element = this.friendsWaiting[index]
            if (userStore.user.id == element.id) {
              this.isFriendsWaiting = true
            } else {
              this.isFriendsWaiting = false
            }
          }
          this.friendsRejected = this.friendsData.rejected
          this.friendsCancelled = this.friendsData.cancelled
          this.friendsNotSend = this.friendsData.notsend
          this.friendsSend = this.friendsData.send
          for (let index = 0; index < this.friendsSend.length; index++) {
            const element = this.friendsSend[index]
            if (userStore.user.id == element.id) {
              this.isFriendsSend = true
            } else {
              this.isFriendsSend = false
            }
          }
          // Store user data
          this.user = response.data.user

          this.friendshipRequests = response.data.requests
          // console.log(`%c${line}`, 'color: #1cd07c; font-size: 16px')
          // console.log('User Friends: ', response.data.user)
          // console.log(`%c${line}`, 'color: #1cd07c; font-size: 16px')
          // console.log('User Friends Requests: ', response.data.requests)
          this.friendship_status = response.data.friendship_status
        })
        .catch((error) => {
          console.log('error', error)
        })
    },
    // 🙏 Send Friend Ship Request
    sendFriendshipRequest() {
      axios
        .post(`/api/friends/${this.$route.params.id}/request/`)
        .then((response) => {
          let line = '🙏'.repeat(30)
          console.log(` %c${line} `, 'color: #1cd07c; font-size: 16px')
          console.log('api/friends id request data', response.data)

          this.can_send_friendship_request = false
          //
          if (response.data.message == 'Friendship request send successfully') {
            this.$toast.add({
              severity: 'success',
              summary: `request Profile`,
              detail: `friendship request created!`,
              life: 3000,
            })
          } else if (response.data.message == 'request already send') {
            this.$toast.add({
              severity: 'success',
              summary: `Error Profile`,
              detail: `The request has already been send!`,
              life: 3000,
            })
          } else {
            this.$toast.add({
              severity: 'error',
              summary: `Error Profile`,
              detail: `The request was send!`,
              life: 3000,
            })
          }
        })
        .catch((error) => {
          console.log('error', error)
        })
    },
    sendFriendshipRequestById(userId) {
      axios
        .post(`/api/friends/${userId}/request/`)
        .then((response) => {
          console.log('api/friends id request data', response.data)

          this.can_send_friendship_request = false
          //
          if (response.data.message == 'Friendship request send successfully') {
            this.$toast.add({
              severity: 'success',
              summary: `request Profile`,
              detail: `friendship request created!`,
              life: 3000,
            })
          } else if (response.data.message == 'request already send') {
            this.$toast.add({
              severity: 'success',
              summary: `Error Profile`,
              detail: `The request has already been send!`,
              life: 3000,
            })
          } else {
            this.$toast.add({
              severity: 'error',
              summary: `Error Profile`,
              detail: `The request was send!`,
              life: 3000,
            })
          }
        })
        .catch((error) => {
          console.log('error', error)
        })
    },
    handleRequest(status, pk) {
      console.log('handleRequest', status)
      axios
        .post(`/api/friends/${pk}/${status}/`)
        .then((response) => {
          this.getFriends()
          console.log('handleRequest MESSAGE', response.data)
          if (response.data.message == 'Friendship request accepted successfully') {
            this.$toast.add({
              severity: 'success',
              summary: `Status ✔️`,
              detail: `Friend Is ${status}`,
              life: 3000,
            })
            // استدعاء دالة تحديث الإشعار كـ "مقروء"
            this.readNotification({ id: response.data.notification_id })
          }
          if (response.data.message == 'Friendship request rejected successfully') {
            this.$toast.add({
              severity: 'error',
              summary: `Status ❌`,
              detail: `Friend Is ${status}`,
              life: 3000,
            })
          }
        })
        .catch((error) => {
          console.log('error', error)
          this.$toast.add({
            severity: 'error',
            summary: `Error Friend Status ❌`,
            detail: `Something went wrong Friend Status`,
            life: 3000,
          })
        })
    },
    getFriendSuggestions() {
      axios
        .get('/api/friends/suggested/')
        .then((response) => {
          this.friendsSuggest = response.data
          // For Test
          let line = '🎁'.repeat(30)
          console.log(` %c${line} `, 'color: #1cd07c; font-size: 16px')
          console.log('get Friend Suggestions() Django Data : ', response.data)
        })
        .catch((error) => {
          console.log('error', error)
        })
    },
    sendDirectMessage() {
      // console.log('sendDirectMessage')
      axios
        .get(`/api/chat/${this.$route.params.id}/get-or-create/`)
        .then((response) => {
          console.log(`chat response.data`, response.data)

          this.$router.push('/')
        })
        .catch((error) => {
          console.log('error', error)
        })
    },
    async readNotification(notification) {
      console.log('readNotification', notification.id)
      await axios
        .post(`/api/notifications/read/${notification.id}/`)
        .then((response) => {
          console.log(response.data)
          console.log(`readNotification ${response.data}`)
        })
        .catch((error) => {
          console.log('Error: ', error)
        })
    },
  },
}
</script>

