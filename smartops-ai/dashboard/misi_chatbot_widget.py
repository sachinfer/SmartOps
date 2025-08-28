"""
Misi AI Chatbot Widget (Floating Popup, WOW UI)
Drop-in replacement keeping the same public API:
    from misi_chatbot_widget import add_misi_to_page
    add_misi_to_page(position="bottom-right")
"""

import streamlit as st
from datetime import datetime

class MisiChatbotWidget:
    def __init__(self, theme_color="#7C3AED"):
        self.theme_color = theme_color  # accent (indigo/violet by default)

    def render_misi_icon(self, position="bottom-right"):
        corner_v, corner_h = position.split("-")
        css = f"""
        <style>
        :root {{
            --misi-accent: {self.theme_color};
            --misi-accent-2: #22C55E;
            --misi-bg: rgba(255,255,255,0.75);
            --misi-border: rgba(255,255,255,0.55);
            --misi-shadow: 0 12px 40px rgba(0,0,0,0.25);
            --misi-dark: #0f172a;
            --misi-light: #f8fafc;
        }}

        @media (prefers-color-scheme: dark) {{
            :root {{
                --misi-bg: rgba(17,24,39,0.7);
                --misi-border: rgba(255,255,255,0.12);
                --misi-light: #0b1220;
            }}
        }}

        .misi-icon-wrap {{
            position: fixed;
            {corner_v}: 22px;
            {corner_h}: 22px;
            z-index: 999999;
        }}

        .misi-fab {{
            width: 64px; height: 64px;
            border-radius: 18px;
            backdrop-filter: blur(10px);
            -webkit-backdrop-filter: blur(10px);
            background: linear-gradient(145deg, var(--misi-accent), #8b5cf6);
            box-shadow: var(--misi-shadow);
            display: grid;
            place-items: center;
            cursor: pointer;
            transition: transform .18s ease, box-shadow .18s ease;
            position: relative;
            animation: misi-pop 420ms cubic-bezier(.2,.7,.2,1) both;
        }}
        .misi-fab:hover {{ transform: translateY(-1px) scale(1.03); }}

        .misi-unread {{
            position: absolute;
            top: -4px; right: -4px;
            width: 18px; height: 18px;
            border-radius: 999px;
            background: var(--misi-accent-2);
            color: white; font: 700 11px/18px ui-sans-serif, system-ui;
            text-align: center;
            box-shadow: 0 6px 16px rgba(34,197,94,.5);
            display:none;
        }}

        .misi-fab-emoji {{ font-size: 26px; color: white; }}

        .misi-popup {{
            position: fixed;
            {corner_v}: 96px;
            {corner_h}: 22px;
            width: 380px; max-width: calc(100vw - 32px);
            height: 560px; max-height: calc(100vh - 140px);
            display: none; flex-direction: column;
            border-radius: 18px;
            background: var(--misi-bg);
            border: 1px solid var(--misi-border);
            box-shadow: var(--misi-shadow);
            overflow: hidden;
            transform-origin: {corner_h} {corner_v};
            animation: misi-pop 300ms cubic-bezier(.2,.7,.2,1) both;
        }}

        @keyframes misi-pop {{
            from {{ opacity: 0; transform: scale(.96); }}
            to   {{ opacity: 1; transform: scale(1); }}
        }}

        .misi-head {{
            background: linear-gradient(160deg, var(--misi-accent), #6d28d9);
            color: white; padding: 14px 14px 12px 14px;
            display: flex; align-items: center; gap: 10px;
        }}
        .misi-head .ttl {{ font: 700 15px/1.1 ui-sans-serif, system-ui; letter-spacing:.2px; }}
        .misi-head .sub {{ font: 500 12px/1 ui-sans-serif, system-ui; opacity:.9; }}
        .misi-head .spacer {{ flex: 1 1 auto; }}
        .misi-btn {{
            background: rgba(255,255,255,.18);
            border: none; color: white; width: 28px; height: 28px;
            border-radius: 9px; cursor: pointer;
        }}
        .misi-btn:hover {{ background: rgba(255,255,255,.28); }}

        .misi-body {{
            flex: 1; overflow-y: auto; padding: 14px;
            background: linear-gradient(180deg, var(--misi-light), transparent 160px);
        }}

        .misi-msg {{ margin: 0 0 10px 0; display:flex; flex-direction:column; }}
        .misi-msg.user {{ align-items: flex-end; }}
        .misi-bubble {{
            max-width: 82%; padding: 10px 14px; border-radius: 16px;
            border: 1px solid rgba(0,0,0,.06);
            background: white; color: #111827;
        }}
        .misi-msg.user .misi-bubble {{
            background: #4f46e5; color: white; border: none;
        }}

        .misi-navcard {{
            margin-top: 6px; padding: 10px 12px; border-radius: 12px;
            border: 1px dashed rgba(99,102,241,.35);
            background: rgba(99,102,241,.08);
            font: 500 12px/1.3 ui-sans-serif, system-ui;
        }}

        .misi-suggest {{ margin-top: 8px; display:flex; flex-wrap:wrap; gap:6px; }}
        .misi-chip {{
            padding: 6px 10px; border-radius: 999px; font: 500 12px ui-sans-serif, system-ui;
            border: 1px solid rgba(0,0,0,.08); background: rgba(255,255,255,.8);
            cursor: pointer;
        }}
        .misi-chip:hover {{ filter: brightness(.97); }}

        .misi-input {{
            display: grid; grid-template-columns: 1fr auto auto; gap: 8px;
            padding: 12px; border-top: 1px solid var(--misi-border); background: rgba(255,255,255,.7);
            backdrop-filter: blur(8px);
        }}
        .misi-text {{
            width: 100%; padding: 10px 12px; border-radius: 12px; border: 1px solid rgba(0,0,0,.12);
            outline: none; font: 500 14px ui-sans-serif, system-ui;
        }}
        .misi-text:focus {{ border-color: var(--misi-accent); box-shadow: 0 0 0 3px rgba(124,58,237,.15); }}
        .misi-send, .misi-mic {{
            min-width: 42px; height: 42px; border-radius: 12px; border: none; cursor: pointer;
            background: var(--misi-accent); color: white; font-size: 18px;
        }}
        .misi-mic {{ background: rgba(0,0,0,.08); color: #111827; }}
        .misi-mic:hover {{ filter: brightness(.95); }}

        @media (max-width: 520px) {{
            .misi-popup {{
                width: calc(100vw - 20px);
                height: min(75vh, 600px);
                {corner_v}: 88px; {corner_h}: 10px;
                border-radius: 16px;
            }}
            .misi-fab {{ width: 58px; height: 58px; border-radius: 16px; }}
        }}
        </style>
        """

        js = """
        <script>
        (function() {
          const state = {
            open: false,
            unread: 0,
            messages: JSON.parse(localStorage.getItem('misi.messages') || '[]')
          };

          function el(id){ return document.getElementById(id); }

          function renderHistory() {
            const body = el('misi-body');
            body.innerHTML = '';
            if (state.messages.length === 0) {
              addMsg('assistant', "Hi! I'm Misi — your SmartOps AI copilot. Ask me about pods, anomalies, shell access, scaling, incidents, or deployments. Try the chips below 👇");
            } else {
              state.messages.forEach(m => appendBubble(m.role, m.content));
            }
            body.scrollTop = body.scrollHeight;
          }

          function appendBubble(role, content) {
            const body = el('misi-body');
            const wrap = document.createElement('div');
            wrap.className = 'misi-msg ' + role;
            const bubble = document.createElement('div');
            bubble.className = 'misi-bubble';
            bubble.textContent = content;
            wrap.appendChild(bubble);
            body.appendChild(wrap);
          }

          function addMsg(role, content) {
            state.messages.push({role, content, t: Date.now()});
            localStorage.setItem('misi.messages', JSON.stringify(state.messages));
            appendBubble(role, content);
            el('misi-body').scrollTop = el('misi-body').scrollHeight;
          }

          function genResponse(q) {
            const map = {
              'pod': 'Open Page 2: Pod Explorer & Logs to inspect status, logs, and health.',
              'anomaly': 'Go to Page 4: Anomaly Detection to review AI-detected incidents.',
              'shell': 'Use Page 3: Kubernetes Shell for direct kubectl access.',
              'scale': 'Page 5 suggests HPA recommendations and controls.',
              'incident': 'Track & document on Page 6: Incident Timeline/Postmortems.',
              'ai': 'Automate runbooks via AI Actions on Page 8.',
              'deploy': 'Monitor rollouts on Page 9: Deployments.'
            };
            const k = Object.keys(map).find(k => q.toLowerCase().includes(k));
            return k ? map[k] : "I can help across SmartOps: pods • anomalies • shell • scaling • incidents • AI actions • deployments. What do you need?";
          }

          function send() {
            const input = el('misi-input-text');
            const v = input.value.trim();
            if (!v) return;
            addMsg('user', v);
            input.value = '';
            setTimeout(() => addMsg('assistant', genResponse(v)), 420);
          }

          function openPopup() {
            if (state.open) return;
            state.open = true;
            el('misi-popup').style.display = 'flex';
            el('misi-unread').style.display = 'none';
            el('misi-input-text').focus();
          }
          function closePopup() {
            if (!state.open) return;
            state.open = false;
            el('misi-popup').style.display = 'none';
          }
          function togglePopup() {
            if (state.open) closePopup(); else openPopup();
          }

          function initChips() {
            const chips = [
              ['Pods', 'pod status'],
              ['Anomalies', 'anomaly overview'],
              ['Shell', 'shell access'],
              ['Scaling', 'scale advice'],
              ['Incidents', 'incident'],
              ['Deployments', 'deploy']
            ];
            const host = el('misi-chips');
            host.innerHTML = '';
            chips.forEach(([label, text]) => {
              const b = document.createElement('button');
              b.className = 'misi-chip';
              b.textContent = label;
              b.addEventListener('click', () => {
                addMsg('user', text);
                setTimeout(() => addMsg('assistant', genResponse(text)), 320);
              });
              host.appendChild(b);
            });
          }

          document.addEventListener('DOMContentLoaded', function(){
            // set up events
            el('misi-fab').addEventListener('click', () => {
              togglePopup();
              if (!state.open) {
                state.unread = Math.min(9, state.unread + 1);
                el('misi-unread').textContent = state.unread;
                el('misi-unread').style.display = 'grid';
              }
            });
            el('misi-close').addEventListener('click', closePopup);
            el('misi-send').addEventListener('click', send);
            el('misi-input-text').addEventListener('keypress', (e) => {
              if (e.key === 'Enter') send();
            });

            // keyboard shortcuts
            document.addEventListener('keydown', (e) => {
              if (e.key.toLowerCase() === 'k' && (e.ctrlKey || e.metaKey)) {
                e.preventDefault(); togglePopup();
              }
              if (e.key === 'Escape') closePopup();
            });

            // click outside to close
            document.addEventListener('click', (e) => {
              const p = el('misi-popup'), f = el('misi-fab');
              if (!p.contains(e.target) && !f.contains(e.target)) closePopup();
            });

            initChips();
            renderHistory();
          });
        })();
        </script>
        """

        html = f"""
        {css}
        <div class="misi-icon-wrap">
          <div class="misi-fab" id="misi-fab" title="Ask Misi (⌘/Ctrl+K)">
            <div class="misi-fab-emoji">🤖</div>
            <div class="misi-unread" id="misi-unread">1</div>
          </div>
        </div>

        <div class="misi-popup" id="misi-popup" role="dialog" aria-label="Misi AI chat">
          <div class="misi-head">
            <div>
              <div class="ttl">Misi • SmartOps</div>
              <div class="sub">AI Copilot is online</div>
            </div>
            <div class="spacer"></div>
            <button class="misi-btn" id="misi-close" aria-label="Close">✕</button>
          </div>

          <div class="misi-body" id="misi-body"></div>

          <div class="misi-navcard" style="margin: 0 12px 6px 12px;">
            Tip: Use <b>⌘/Ctrl + K</b> to toggle, <b>Esc</b> to close.
            <div class="misi-suggest" id="misi-chips"></div>
          </div>

          <div class="misi-input">
            <input id="misi-input-text" class="misi-text" placeholder="Ask me anything about SmartOps…" />
            <button class="misi-mic" title="Voice (coming soon)">🎙️</button>
            <button class="misi-send" id="misi-send" title="Send">➤</button>
          </div>
        </div>
        {js}
        """
        st.markdown(html, unsafe_allow_html=True)

    def render_misi_integration(self, position="bottom-right"):
        if 'misi_messages' not in st.session_state:
            st.session_state.misi_messages = [
                {"role": "assistant",
                 "content": "Hi! I'm Misi, your SmartOps AI assistant. How can I help you today?",
                 "timestamp": datetime.now()}
            ]
        self.render_misi_icon(position)

def add_misi_to_page(position="bottom-right", theme_color="#7C3AED"):
    misi = MisiChatbotWidget(theme_color=theme_color)
    misi.render_misi_integration(position)
    return misi
