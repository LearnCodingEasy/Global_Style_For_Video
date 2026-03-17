<script setup>
/**
 * MCPDashboard.vue
 * src/pages/mcp/MCPDashboard.vue
 *
 * MCP Server monitoring dashboard.
 * Shows: connected agents, tool usage, logs, token management.
 */
import { ref, computed, onMounted, onUnmounted } from 'vue'
import { useToast } from 'primevue/usetoast'
import mcpService from '@/services/mcpService'

const toast = useToast()

// ── State ─────────────────────────────────────────────────
const sessions = ref([])
const tools = ref([])
const toolStats = ref({})
const logs = ref([])
const loading = ref(false)
const activeTab = ref(0)
const showToken = ref(false)
const newTokenName = ref('My Agent')
const generatedToken = ref(null)
let refreshInterval = null

// ── Computed ──────────────────────────────────────────────
const totalRequests = computed(() =>
  Object.values(toolStats.value).reduce((sum, s) => sum + (s.calls || 0), 0),
)

const topTools = computed(() =>
  Object.entries(toolStats.value)
    .map(([name, s]) => ({ name, calls: s.calls }))
    .sort((a, b) => b.calls - a.calls)
    .slice(0, 5),
)

const toolsByCategory = computed(() => {
  const groups = {}
  for (const tool of tools.value) {
    if (!groups[tool.category]) groups[tool.category] = []
    groups[tool.category].push(tool)
  }
  return groups
})

const categoryColors = {
  workflows: '#22c55e',
  programs: '#3b82f6',
  desktop: '#f59e0b',
  system: '#8b5cf6',
  general: '#64748b',
}

// ── Data Loading ──────────────────────────────────────────
const loadAll = async () => {
  loading.value = true
  try {
    const [sessData, toolData, logData] = await Promise.all([
      mcpService.getSessions(),
      mcpService.getTools(),
      mcpService.getLogs(30),
    ])
    sessions.value = sessData.sessions || []
    toolStats.value = sessData.tool_stats || {}
    tools.value = toolData.tools || []
    logs.value = logData.logs || []
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Load Failed', detail: e.message, life: 4000 })
  } finally {
    loading.value = false
  }
}

// ── Tool Toggle ───────────────────────────────────────────
const toggleTool = async (tool) => {
  const prev = tool.enabled
  tool.enabled = !prev
  try {
    await mcpService.setToolEnabled(tool.name, tool.enabled)
    toast.add({
      severity: tool.enabled ? 'success' : 'warn',
      summary: tool.enabled ? '✅ Tool Enabled' : '⏸ Tool Disabled',
      detail: tool.name,
      life: 3000,
    })
  } catch (e) {
    tool.enabled = prev
    toast.add({ severity: 'error', summary: 'Failed', detail: e.message, life: 4000 })
  }
}

// ── Token Management ──────────────────────────────────────
const generateToken = async () => {
  try {
    const result = await mcpService.createToken(newTokenName.value)
    generatedToken.value = result.token
    showToken.value = true
    toast.add({
      severity: 'success',
      summary: '🔑 Token Created',
      detail: 'Copy it now — shown once',
      life: 5000,
    })
  } catch (e) {
    toast.add({ severity: 'error', summary: 'Failed', detail: e.message, life: 4000 })
  }
}

const copyToken = async () => {
  await navigator.clipboard.writeText(generatedToken.value)
  toast.add({ severity: 'info', summary: 'Copied!', life: 2000 })
}

// ── Helpers ───────────────────────────────────────────────
const timeAgo = (isoStr) => {
  if (!isoStr) return 'Never'
  const diff = Date.now() - new Date(isoStr).getTime()
  const s = Math.floor(diff / 1000)
  if (s < 60) return `${s}s ago`
  if (s < 3600) return `${Math.floor(s / 60)}m ago`
  if (s < 86400) return `${Math.floor(s / 3600)}h ago`
  return `${Math.floor(s / 86400)}d ago`
}

const logSeverity = (log) => (log.success ? 'success' : 'error')
console.log('logSeverity: ', logSeverity)

const tabs = [
  { label: 'Overview', icon: 'pi pi-home' },
  { label: 'Agents', icon: 'pi pi-users' },
  { label: 'Tools', icon: 'pi pi-bolt' },
  { label: 'Logs', icon: 'pi pi-list' },
  { label: 'Tokens', icon: 'pi pi-key' },
]

// ── Lifecycle ─────────────────────────────────────────────
onMounted(() => {
  loadAll()
  refreshInterval = setInterval(loadAll, 10000) // refresh every 10s
})

onUnmounted(() => clearInterval(refreshInterval))
</script>

<template>
  <div class="mcp-dashboard">
    <!-- ── Page Header ────────────────────────────────── -->
    <div class="mcp-header">
      <div class="mcp-header__left">
        <div class="mcp-logo">
          <i class="pi pi-server"></i>
        </div>
        <div>
          <h1 class="mcp-title">MCP Server</h1>
          <p class="mcp-subtitle">Model Context Protocol — AI Agent Interface</p>
        </div>
      </div>

      <div class="mcp-header__right">
        <div class="mcp-status-badge" :class="sessions.length ? 'active' : 'idle'">
          <span class="status-dot"></span>
          {{
            sessions.length
              ? `${sessions.length} Agent${sessions.length > 1 ? 's' : ''} Connected`
              : 'No Agents'
          }}
        </div>
        <prime_button
          icon="pi pi-refresh"
          size="small"
          outlined
          :loading="loading"
          @click="loadAll"
          v-tooltip="'Refresh'"
        />
      </div>
    </div>

    <!-- ── Tab Navigation ────────────────────────────── -->
    <div class="mcp-tabs">
      <button
        v-for="(tab, i) in tabs"
        :key="tab.label"
        class="mcp-tab"
        :class="{ 'mcp-tab--active': activeTab === i }"
        @click="activeTab = i"
      >
        <i :class="tab.icon"></i>
        <span>{{ tab.label }}</span>
      </button>
    </div>

    <!-- ══════════════════════════════════════════════════
         TAB 0 — OVERVIEW
    ══════════════════════════════════════════════════ -->
    <div v-if="activeTab === 0" class="tab-content">
      <!-- Stats Cards -->
      <div class="stats-grid">
        <div class="stat-card">
          <div class="stat-value" style="color: #22c55e">{{ sessions.length }}</div>
          <div class="stat-label">Active Agents</div>
          <i class="pi pi-users stat-icon" style="color: #22c55e22"></i>
        </div>
        <div class="stat-card">
          <div class="stat-value" style="color: #3b82f6">{{ tools.length }}</div>
          <div class="stat-label">Tools Registered</div>
          <i class="pi pi-bolt stat-icon" style="color: #3b82f622"></i>
        </div>
        <div class="stat-card">
          <div class="stat-value" style="color: #f59e0b">{{ totalRequests }}</div>
          <div class="stat-label">Total Requests</div>
          <i class="pi pi-chart-bar stat-icon" style="color: #f59e0b22"></i>
        </div>
        <div class="stat-card">
          <div class="stat-value" style="color: #8b5cf6">
            {{ tools.filter((t) => t.enabled).length }}
          </div>
          <div class="stat-label">Enabled Tools</div>
          <i class="pi pi-check-circle stat-icon" style="color: #8b5cf622"></i>
        </div>
      </div>

      <!-- Top Tools Chart -->
      <div class="section-card">
        <h3 class="section-title">📊 Top Tools by Usage</h3>
        <div v-if="!topTools.length" class="empty-hint">No tool calls recorded yet.</div>
        <div v-else class="tool-bars">
          <div v-for="t in topTools" :key="t.name" class="tool-bar-row">
            <span class="tool-bar-name">{{ t.name }}</span>
            <div class="tool-bar-track">
              <div
                class="tool-bar-fill"
                :style="{
                  width: topTools[0].calls ? (t.calls / topTools[0].calls) * 100 + '%' : '0%',
                  background: '#3b82f6',
                }"
              ></div>
            </div>
            <span class="tool-bar-count">{{ t.calls }}</span>
          </div>
        </div>
      </div>

      <!-- Recent Logs Preview -->
      <div class="section-card">
        <h3 class="section-title">🕒 Recent Activity</h3>
        <div v-if="!logs.length" class="empty-hint">No activity yet.</div>
        <div v-else class="log-list">
          <div v-for="log in logs.slice(0, 8)" :key="log.id" class="log-row">
            <span class="log-icon" :class="log.success ? 'success' : 'error'">
              {{ log.success ? '✅' : '❌' }}
            </span>
            <span class="log-tool">{{ log.tool_name }}</span>
            <span class="log-duration">{{ log.duration_ms }}ms</span>
            <span class="log-time">{{ timeAgo(log.started_at) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════
         TAB 1 — AGENTS
    ══════════════════════════════════════════════════ -->
    <div v-else-if="activeTab === 1" class="tab-content">
      <div class="section-card">
        <h3 class="section-title">🤖 Connected Agents</h3>

        <div v-if="!sessions.length" class="empty-state">
          <i class="pi pi-users" style="font-size: 2.5rem; color: #334155"></i>
          <p class="empty-hint">No agents connected. Use a token to connect an AI agent.</p>
        </div>

        <div v-else class="agents-table">
          <div class="table-header">
            <span>Agent</span>
            <span>IP</span>
            <span>Requests</span>
            <span>Last Seen</span>
            <span>Expires</span>
          </div>
          <div v-for="s in sessions" :key="s.id" class="table-row">
            <div class="agent-name-cell">
              <div class="agent-avatar">
                <i class="pi pi-android"></i>
              </div>
              <div>
                <div class="agent-name">{{ s.agent_name || 'Unknown Agent' }}</div>
                <div class="agent-version" v-if="s.agent_version">v{{ s.agent_version }}</div>
              </div>
            </div>
            <span class="table-cell mono">{{ s.ip_address || '—' }}</span>
            <span class="table-cell">
              <prime_tag :value="String(s.request_count)" severity="info" />
            </span>
            <span class="table-cell text-muted">{{ timeAgo(s.last_seen) }}</span>
            <span class="table-cell text-muted">{{ timeAgo(s.expires_at) }}</span>
          </div>
        </div>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════
         TAB 2 — TOOLS
    ══════════════════════════════════════════════════ -->
    <div v-else-if="activeTab === 2" class="tab-content">
      <div
        v-for="(categoryTools, category) in toolsByCategory"
        :key="category"
        class="section-card"
      >
        <h3 class="section-title">
          <span
            class="category-dot"
            :style="{ background: categoryColors[category] || '#64748b' }"
          ></span>
          {{ category.charAt(0).toUpperCase() + category.slice(1) }} Tools
        </h3>

        <div class="tools-grid">
          <div
            v-for="tool in categoryTools"
            :key="tool.name"
            class="tool-card"
            :class="{ 'tool-card--disabled': !tool.enabled }"
          >
            <div class="tool-card__header">
              <div class="tool-name">{{ tool.name }}</div>
              <prime_toggle_switch
                :model-value="tool.enabled"
                @update:model-value="toggleTool(tool)"
              />
            </div>
            <p class="tool-desc">{{ tool.description }}</p>
            <div class="tool-meta">
              <prime_tag
                :value="category"
                :style="{
                  background: (categoryColors[category] || '#64748b') + '22',
                  color: categoryColors[category] || '#64748b',
                  border: 'none',
                }"
                class="!text-xs"
              />
              <span class="tool-calls"> {{ toolStats[tool.name]?.calls || 0 }} calls </span>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ════════════════════════════════════════════
    TAB 3 — LOGS
    ═════════════════════════════════════════════ -->
    <div v-else-if="activeTab === 3" class="tab-content">
      <div class="section-card">
        <h3 class="section-title">📋 Tool Call Logs</h3>

        <div v-if="!logs.length" class="empty-hint">No logs yet.</div>

        <div v-else class="logs-full">
          <div v-for="log in logs" :key="log.id" class="log-entry">
            <div class="log-entry__header">
              <span :class="['log-status', log.success ? 'log-status--ok' : 'log-status--err']">
                {{ log.success ? '✅' : '❌' }}
              </span>
              <span class="log-tool-name">{{ log.tool_name }}</span>
              <prime_tag
                v-if="log.duration_ms"
                :value="`${log.duration_ms}ms`"
                severity="secondary"
                class="!text-xs"
              />
              <span class="log-time-stamp">{{ timeAgo(log.started_at) }}</span>
            </div>

            <!-- Args -->
            <div class="log-entry__body">
              <div class="log-section-label">Arguments</div>
              <pre class="log-code">{{ JSON.stringify(log.arguments, null, 2) }}</pre>

              <!-- Result or Error -->
              <template v-if="log.success && log.result">
                <div class="log-section-label success-label">Result</div>
                <pre class="log-code log-code--success">{{
                  JSON.stringify(log.result, null, 2)
                }}</pre>
              </template>
              <template v-if="!log.success && log.error">
                <div class="log-section-label error-label">Error</div>
                <pre class="log-code log-code--error">{{ log.error }}</pre>
              </template>
            </div>
          </div>
        </div>
      </div>
    </div>

    <!-- ══════════════════════════════════════════════════
         TAB 4 — TOKENS
    ══════════════════════════════════════════════════ -->
    <div v-else-if="activeTab === 4" class="tab-content">
      <div class="section-card">
        <h3 class="section-title">🔑 API Token Management</h3>

        <!-- Generate Token Form -->
        <div class="token-form">
          <div class="field">
            <label class="field-label">Token Name / Agent Name</label>
            <prime_input_text
              v-model="newTokenName"
              placeholder="e.g. Claude Desktop, My AI Agent"
              class="w-full"
            />
          </div>
          <prime_button
            label="Generate Token"
            icon="pi pi-key"
            @click="generateToken"
            severity="info"
          />
        </div>

        <!-- Generated Token Display -->
        <div v-if="showToken && generatedToken" class="token-display">
          <div class="token-display__header">
            <span>🔐 Your Token</span>
            <prime_tag value="Copy & Store Securely" severity="warn" />
          </div>
          <div class="token-value">
            <code>{{ generatedToken }}</code>
            <prime_button
              icon="pi pi-copy"
              size="small"
              text
              @click="copyToken"
              v-tooltip="'Copy'"
            />
          </div>
          <p class="token-warning">⚠️ This token will not be shown again. Store it securely.</p>
        </div>

        <!-- Usage Instructions -->
        <div class="token-usage">
          <h4 class="section-title">📖 How to Connect an Agent</h4>
          <pre class="log-code">{{ usageExample }}</pre>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
// Usage example shown in Tokens tab
const usageExample = `# 1. Initialize MCP connection
POST /api/mcp/
Authorization: Bearer YOUR_TOKEN

{
  "jsonrpc": "2.0",
  "method": "initialize",
  "id": 1,
  "params": {
    "protocolVersion": "2024-11-05",
    "clientInfo": { "name": "MyAgent", "version": "1.0" }
  }
}

# 2. List available tools
{ "jsonrpc": "2.0", "method": "tools/list", "id": 2 }

# 3. Execute a workflow
{
  "jsonrpc": "2.0",
  "method": "tools/call",
  "id": 3,
  "params": {
    "name": "run_workflow",
    "arguments": { "workflow_id": "YOUR_WORKFLOW_UUID" }
  }
}`
</script>

<style scoped>
/* ── Dashboard Layout ─────────────────────────────────── */
.mcp-dashboard {
  padding: 24px;
  min-height: 100vh;
  background: #0a0f1a;
  color: #e2e8f0;
}

/* ── Header ───────────────────────────────────────────── */
.mcp-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 24px;
}

.mcp-header__left {
  display: flex;
  align-items: center;
  gap: 14px;
}

.mcp-logo {
  width: 48px;
  height: 48px;
  border-radius: 12px;
  background: linear-gradient(135deg, #3b82f6, #8b5cf6);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.4rem;
  color: white;
}

.mcp-title {
  font-size: 1.4rem;
  font-weight: 700;
  margin: 0;
  color: #f1f5f9;
}
.mcp-subtitle {
  font-size: 0.8rem;
  color: #64748b;
  margin: 0;
}

.mcp-header__right {
  display: flex;
  align-items: center;
  gap: 10px;
}

.mcp-status-badge {
  display: flex;
  align-items: center;
  gap: 7px;
  padding: 6px 14px;
  border-radius: 20px;
  font-size: 0.8rem;
  font-weight: 500;
}

.mcp-status-badge.active {
  background: rgba(34, 197, 94, 0.1);
  border: 1px solid rgba(34, 197, 94, 0.3);
  color: #4ade80;
}

.mcp-status-badge.idle {
  background: rgba(100, 116, 139, 0.1);
  border: 1px solid rgba(100, 116, 139, 0.3);
  color: #94a3b8;
}

.status-dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: currentColor;
  animation: pulse-dot 2s ease-in-out infinite;
}

@keyframes pulse-dot {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.3;
  }
}

/* ── Tabs ─────────────────────────────────────────────── */
.mcp-tabs {
  display: flex;
  gap: 4px;
  margin-bottom: 20px;
  border-bottom: 1px solid #1e293b;
  padding-bottom: 0;
}

.mcp-tab {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 10px 16px;
  background: transparent;
  border: none;
  border-bottom: 2px solid transparent;
  color: #64748b;
  cursor: pointer;
  font-size: 0.82rem;
  font-weight: 500;
  transition: all 0.15s;
  margin-bottom: -1px;
}

.mcp-tab:hover {
  color: #94a3b8;
}
.mcp-tab--active {
  color: #60a5fa;
  border-bottom-color: #60a5fa;
}

/* ── Content Sections ─────────────────────────────────── */
.tab-content {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.section-card {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 20px;
}

.section-title {
  font-size: 0.9rem;
  font-weight: 600;
  color: #94a3b8;
  margin: 0 0 16px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.category-dot {
  display: inline-block;
  width: 10px;
  height: 10px;
  border-radius: 50%;
}

/* ── Stats Grid ───────────────────────────────────────── */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-card {
  background: #1e293b;
  border: 1px solid #334155;
  border-radius: 12px;
  padding: 20px;
  position: relative;
  overflow: hidden;
}

.stat-value {
  font-size: 2rem;
  font-weight: 700;
}
.stat-label {
  font-size: 0.75rem;
  color: #64748b;
  margin-top: 4px;
}

.stat-icon {
  position: absolute;
  right: 16px;
  bottom: 12px;
  font-size: 2.5rem;
}

/* ── Tool Bars ────────────────────────────────────────── */
.tool-bars {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.tool-bar-row {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.8rem;
}

.tool-bar-name {
  width: 160px;
  color: #94a3b8;
}
.tool-bar-track {
  flex: 1;
  height: 8px;
  background: #0f172a;
  border-radius: 4px;
  overflow: hidden;
}
.tool-bar-fill {
  height: 100%;
  border-radius: 4px;
  transition: width 0.5s ease;
}
.tool-bar-count {
  width: 40px;
  text-align: right;
  color: #64748b;
}

/* ── Log List ─────────────────────────────────────────── */
.log-list {
  display: flex;
  flex-direction: column;
  gap: 6px;
}

.log-row {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 6px 0;
  border-bottom: 1px solid rgba(255, 255, 255, 0.04);
  font-size: 0.8rem;
}

.log-icon.success {
  color: #4ade80;
}
.log-icon.error {
  color: #f87171;
}
.log-tool {
  flex: 1;
  color: #e2e8f0;
}
.log-duration {
  color: #64748b;
  width: 50px;
  text-align: right;
}
.log-time {
  color: #475569;
  width: 70px;
  text-align: right;
}

/* ── Agents Table ─────────────────────────────────────── */
.agents-table {
  display: flex;
  flex-direction: column;
}

.table-header {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr;
  gap: 12px;
  padding: 8px 12px;
  font-size: 0.7rem;
  text-transform: uppercase;
  color: #475569;
  letter-spacing: 0.06em;
}

.table-row {
  display: grid;
  grid-template-columns: 2fr 1fr 1fr 1fr 1fr;
  gap: 12px;
  padding: 12px;
  border-top: 1px solid #1e293b;
  align-items: center;
  font-size: 0.82rem;
}

.agent-name-cell {
  display: flex;
  align-items: center;
  gap: 10px;
}
.agent-avatar {
  width: 32px;
  height: 32px;
  background: #334155;
  border-radius: 8px;
  display: flex;
  align-items: center;
  justify-content: center;
  color: #94a3b8;
}
.agent-name {
  font-weight: 600;
  color: #e2e8f0;
}
.agent-version {
  font-size: 0.7rem;
  color: #64748b;
}
.table-cell {
  color: #94a3b8;
}
.text-muted {
  color: #475569;
}
.mono {
  font-family: monospace;
}

/* ── Tools Grid ───────────────────────────────────────── */
.tools-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 12px;
}

.tool-card {
  background: #0f172a;
  border: 1px solid #334155;
  border-radius: 10px;
  padding: 14px;
  transition: opacity 0.2s;
}

.tool-card--disabled {
  opacity: 0.5;
}

.tool-card__header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 6px;
}

.tool-name {
  font-weight: 600;
  font-size: 0.82rem;
  color: #e2e8f0;
}
.tool-desc {
  font-size: 0.72rem;
  color: #64748b;
  margin: 0 0 8px;
  line-height: 1.4;
}
.tool-meta {
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.tool-calls {
  font-size: 0.7rem;
  color: #475569;
}

/* ── Full Logs ────────────────────────────────────────── */
.logs-full {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.log-entry {
  background: #0f172a;
  border: 1px solid #1e293b;
  border-radius: 8px;
  overflow: hidden;
}

.log-entry__header {
  display: flex;
  align-items: center;
  gap: 10px;
  padding: 10px 14px;
  background: rgba(255, 255, 255, 0.02);
}

.log-status {
  font-size: 0.9rem;
}
.log-tool-name {
  flex: 1;
  font-weight: 600;
  font-size: 0.82rem;
  color: #e2e8f0;
}
.log-time-stamp {
  font-size: 0.72rem;
  color: #475569;
}

.log-entry__body {
  padding: 12px 14px;
}
.log-section-label {
  font-size: 0.65rem;
  text-transform: uppercase;
  color: #475569;
  letter-spacing: 0.08em;
  margin-bottom: 4px;
  margin-top: 8px;
}
.success-label {
  color: #4ade80;
}
.error-label {
  color: #f87171;
}

.log-code {
  background: #0a0f1a;
  border: 1px solid #1e293b;
  border-radius: 6px;
  padding: 10px 12px;
  font-size: 0.72rem;
  color: #94a3b8;
  overflow-x: auto;
  white-space: pre-wrap;
  word-break: break-word;
  margin: 0;
}

.log-code--success {
  border-color: rgba(34, 197, 94, 0.2);
  color: #4ade80;
}
.log-code--error {
  border-color: rgba(239, 68, 68, 0.2);
  color: #f87171;
}

/* ── Token Management ─────────────────────────────────── */
.token-form {
  display: flex;
  align-items: flex-end;
  gap: 12px;
  margin-bottom: 20px;
}

.field {
  display: flex;
  flex-direction: column;
  gap: 6px;
  flex: 1;
}
.field-label {
  font-size: 0.78rem;
  color: #94a3b8;
}

.token-display {
  background: rgba(234, 179, 8, 0.08);
  border: 1px solid rgba(234, 179, 8, 0.3);
  border-radius: 10px;
  padding: 16px;
  margin-bottom: 20px;
}

.token-display__header {
  display: flex;
  align-items: center;
  gap: 10px;
  font-size: 0.85rem;
  font-weight: 600;
  color: #fbbf24;
  margin-bottom: 10px;
}

.token-value {
  display: flex;
  align-items: center;
  gap: 10px;
  background: #0f172a;
  border-radius: 6px;
  padding: 10px 14px;
}

.token-value code {
  flex: 1;
  font-family: monospace;
  font-size: 0.78rem;
  color: #e2e8f0;
  word-break: break-all;
}

.token-warning {
  font-size: 0.75rem;
  color: #f59e0b;
  margin: 10px 0 0;
}

.token-usage pre {
  margin-top: 8px;
}

/* ── Empty States ─────────────────────────────────────── */
.empty-hint {
  font-size: 0.8rem;
  color: #475569;
  text-align: center;
  padding: 24px;
}
.empty-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 10px;
  padding: 40px;
}
</style>
