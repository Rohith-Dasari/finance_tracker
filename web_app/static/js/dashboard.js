(() => {
	const chatInput = document.getElementById('chat-input');
	const chatSend = document.getElementById('chat-send');
	const chatLog = document.getElementById('chat-log');

	if (!chatInput || !chatSend || !chatLog) return;

	async function sendChat() {
		const message = chatInput.value.trim();
		if (!message) return;
		appendEntry('You', message);
		chatInput.value = '';

		try {
			const res = await fetch('/api/chat', {
				method: 'POST',
				headers: { 'Content-Type': 'application/json' },
				body: JSON.stringify({ message }),
			});
			const data = await res.json();
			if (!res.ok) {
				appendEntry('Error', data.error || 'Request failed');
				return;
			}
			appendEntry('Assistant', data.reply || '(no reply)');
		} catch (err) {
			appendEntry('Error', err.message || 'Network error');
		}
	}

	function appendEntry(author, text) {
		const role = author.toLowerCase().includes('error')
			? 'error'
			: author.toLowerCase() === 'assistant'
				? 'assistant'
				: 'user';

		const entry = document.createElement('div');
		entry.className = 'chat-entry';
		entry.dataset.role = role;

		const meta = document.createElement('div');
		meta.className = 'chat-meta';
		meta.textContent = author;

		const message = document.createElement('div');
		message.className = 'chat-message';
		message.textContent = text;

		entry.appendChild(meta);
		entry.appendChild(message);
		chatLog.appendChild(entry);
		chatLog.scrollTop = chatLog.scrollHeight;
	}

	chatSend.addEventListener('click', sendChat);
	chatInput.addEventListener('keydown', (e) => {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			sendChat();
		}
	});
})();
