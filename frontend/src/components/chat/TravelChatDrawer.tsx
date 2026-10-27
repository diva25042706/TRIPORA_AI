import React, { useState, useEffect, useRef } from 'react';
import { MessageSquare, X, Send, Sparkles, Bot, User as UserIcon, RefreshCw } from 'lucide-react';
import { tripService } from '../../services/tripService';
import { ChatMessage } from '../../types';

interface TravelChatDrawerProps {
  tripId: string;
  destination: string;
}

export const TravelChatDrawer: React.FC<TravelChatDrawerProps> = ({ tripId, destination }) => {
  const [isOpen, setIsOpen] = useState<boolean>(false);
  const [messages, setMessages] = useState<ChatMessage[]>([]);
  const [inputMessage, setInputMessage] = useState<string>('');
  const [isSending, setIsSending] = useState<boolean>(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (isOpen) {
      loadHistory();
    }
  }, [isOpen, tripId]);

  useEffect(() => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages]);

  const loadHistory = async () => {
    try {
      const history = await tripService.getChatHistory(tripId);
      if (history.length === 0) {
        // Seed welcome greeting
        setMessages([
          {
            id: 0,
            role: 'assistant',
            content: `Hello! I am your TRIPORA AI Travel Assistant. I am directly grounded in your ${destination} itinerary, weather forecasts, and budget breakdown. What would you like to know or adjust?`,
            agent_name: 'TRIPORA Assistant',
            created_at: new Date().toISOString(),
          },
        ]);
      } else {
        setMessages(history);
      }
    } catch (err) {
      console.error('Failed to load chat history:', err);
    }
  };

  const handleSend = async (textToSend?: string) => {
    const text = textToSend || inputMessage;
    if (!text.trim() || isSending) return;

    setInputMessage('');
    const tempUserMsg: ChatMessage = {
      id: Date.now(),
      role: 'user',
      content: text,
      agent_name: 'You',
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, tempUserMsg]);
    setIsSending(true);

    try {
      const botResponse = await tripService.sendChatMessage(tripId, text);
      setMessages((prev) => [...prev, botResponse]);
    } catch (err) {
      console.error('Chat error:', err);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          role: 'assistant',
          content: 'Sorry, I encountered a temporary connection issue. Please retry your message.',
          agent_name: 'TRIPORA Assistant',
          created_at: new Date().toISOString(),
        },
      ]);
    } finally {
      setIsSending(false);
    }
  };

  const quickPrompts = [
    'How is my total budget divided?',
    'What should I pack given the weather forecast?',
    'Explain the schedule for Day 1',
    'Which hotel was recommended and why?',
  ];

  return (
    <>
      {/* Floating Action Trigger Button */}
      {!isOpen && (
        <button
          onClick={() => setIsOpen(true)}
          className="fixed bottom-6 right-6 z-40 px-5 py-3 rounded-full bg-[#143628] hover:bg-[#1E4D3B] text-white shadow-xl flex items-center gap-2.5 transition-all hover:scale-105 border border-[#10B981]/30"
        >
          <div className="relative">
            <MessageSquare className="w-5 h-5 text-[#10B981]" />
            <span className="absolute -top-1 -right-1 w-2.5 h-2.5 bg-[#10B981] rounded-full animate-ping" />
          </div>
          <span className="text-xs font-bold tracking-wide">Ask Trip AI Assistant</span>
        </button>
      )}

      {/* Floating Chat Drawer */}
      {isOpen && (
        <div className="fixed bottom-6 right-6 z-50 w-full max-w-md h-[560px] bg-white rounded-3xl border border-[#E7E5DF] shadow-2xl flex flex-col overflow-hidden animate-slide-up">
          {/* Header */}
          <div className="p-4 bg-[#FAF9F5] border-b border-[#E7E5DF] flex items-center justify-between">
            <div className="flex items-center gap-2.5">
              <div className="w-8 h-8 rounded-lg bg-[#143628] flex items-center justify-center text-[#10B981]">
                <Bot className="w-4 h-4" />
              </div>
              <div>
                <h4 className="text-sm font-bold text-[#0F1E28]">
                  TRIPORA Trip Concierge
                </h4>
                <span className="text-[10px] text-[#059669] font-medium flex items-center gap-1">
                  <span className="w-1.5 h-1.5 rounded-full bg-[#10B981]" /> Grounded in {destination} Plan
                </span>
              </div>
            </div>
            <button
              onClick={() => setIsOpen(false)}
              className="p-1.5 text-[#5A6D7C] hover:text-[#0F1E28] hover:bg-black/5 rounded-full transition-colors"
            >
              <X className="w-4 h-4" />
            </button>
          </div>

          {/* Messages Area */}
          <div className="flex-1 p-4 overflow-y-auto space-y-3 bg-[#FAF9F5]/40 text-xs">
            {messages.map((m) => (
              <div
                key={m.id}
                className={`flex gap-2.5 ${m.role === 'user' ? 'justify-end' : 'justify-start'}`}
              >
                {m.role !== 'user' && (
                  <div className="w-7 h-7 rounded-full bg-[#143628] text-[#10B981] flex items-center justify-center shrink-0 mt-0.5">
                    <Sparkles className="w-3.5 h-3.5" />
                  </div>
                )}
                <div
                  className={`max-w-[80%] p-3 rounded-2xl leading-relaxed ${
                    m.role === 'user'
                      ? 'bg-[#143628] text-white rounded-br-none'
                      : 'bg-white text-[#2C3E50] border border-[#E7E5DF] rounded-bl-none shadow-sm'
                  }`}
                >
                  <p className="whitespace-pre-wrap">{m.content}</p>
                </div>
              </div>
            ))}
            {isSending && (
              <div className="flex items-center gap-2 text-[#5A6D7C] text-[11px] p-2 bg-white rounded-xl border border-[#E7E5DF] max-w-[200px]">
                <RefreshCw className="w-3.5 h-3.5 animate-spin text-[#10B981]" />
                <span>Consulting trip state...</span>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Quick Prompt Suggestions */}
          <div className="px-4 py-2 bg-white border-t border-[#F1F0EB] flex gap-1.5 overflow-x-auto scrollbar-none">
            {quickPrompts.map((prompt, idx) => (
              <button
                key={idx}
                type="button"
                onClick={() => handleSend(prompt)}
                className="px-2.5 py-1 rounded-full bg-[#FAF9F5] hover:bg-[#10B981]/10 text-[10px] font-medium text-[#2C3E50] border border-[#E7E5DF] whitespace-nowrap transition-colors"
              >
                {prompt}
              </button>
            ))}
          </div>

          {/* Input Form */}
          <form
            onSubmit={(e) => {
              e.preventDefault();
              handleSend();
            }}
            className="p-3 bg-white border-t border-[#E7E5DF] flex items-center gap-2"
          >
            <input
              type="text"
              value={inputMessage}
              onChange={(e) => setInputMessage(e.target.value)}
              placeholder="Ask a question about your trip..."
              className="flex-1 px-3.5 py-2 rounded-xl border border-[#CBD5E1] text-xs focus:outline-none focus:ring-1 focus:ring-[#10B981]"
            />
            <button
              type="submit"
              disabled={!inputMessage.trim() || isSending}
              className="p-2 rounded-xl bg-[#143628] hover:bg-[#1E4D3B] text-white disabled:opacity-40 transition-colors shadow-sm"
            >
              <Send className="w-4 h-4" />
            </button>
          </form>
        </div>
      )}
    </>
  );
};
