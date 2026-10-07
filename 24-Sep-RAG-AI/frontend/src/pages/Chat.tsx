import { useState, useRef, useEffect } from "react";
import {
    Bot,
    Database,
    Menu,
    Send,
    Settings,
    User,
} from "lucide-react";

import { Button } from "@/components/ui/button";
import { Badge } from "@/components/ui/badge";
import { Input } from "@/components/ui/input";

interface Message {
    id?: string;
    sender?: "user" | "assistant";
    text?: string;
    role?: "user" | "assistant";
    content?: string;
}

interface HistoryItem {
  id: number;
  question: string;
  answer: string;
  created_at: string;
}

export default function Chat() {
    const [messages, setMessages] = useState<Message[]>([
        {
            id: "welcome-ai",
            sender: "assistant",
            text: "Hello! How can I help you today?",
        },
    ]);

    const [inputQuery, setInputQuery] = useState("");
    const [isLoading, setIsLoading] = useState(false);
    const messagesEndRef = useRef<HTMLDivElement>(null);

    useEffect(() => {
        const loadHistory = async () => {
            try {
                const response = await fetch(
                    "http://localhost:8000/history"
                );

                if (!response.ok) {
                    throw new Error("Failed to load chat history");
                }

                const data = await response.json();

                const historyMessages: Message[] =
                    data.history.flatMap((item: HistoryItem) => [
                        {
                            role: "user",
                            content: item.question,
                        },
                        {
                            role: "assistant",
                            content: item.answer,
                        },
                    ]);

                setMessages(historyMessages);
            } catch (error) {
                console.error("History error:", error);
            }
        };

        loadHistory();
    }, []);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages, isLoading]);

    const handleSendMessage = async () => {
        const trimmed = inputQuery.trim();
        if (!trimmed || isLoading) return;

        const userMsg: Message = {
            id: `user-${Date.now()}`,
            sender: "user",
            text: trimmed,
        };

        setMessages((prev) => [...prev, userMsg]);
        setInputQuery("");
        setIsLoading(true);

        try {
            const response = await fetch("http://localhost:8000/chat", {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({ question: trimmed }),
            });

            if (!response.ok) {
                const errData = await response.json().catch(() => ({}));
                throw new Error(errData.detail || `Server error (${response.status})`);
            }

            const data = await response.json();

            const aiMsg: Message = {
                id: `ai-${Date.now()}`,
                sender: "assistant",
                text: data.answer || "No response received from SQL agent.",
            };

            setMessages((prev) => [...prev, aiMsg]);
        } catch (err: any) {
            const errorMsg: Message = {
                id: `err-${Date.now()}`,
                sender: "assistant",
                text: `Error connecting to backend: ${err.message}. Make sure the backend is running on http://localhost:8000.`,
            };
            setMessages((prev) => [...prev, errorMsg]);
        } finally {
            setIsLoading(false);
        }
    };

    const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
        if (e.key === "Enter" && !e.shiftKey) {
            e.preventDefault();
            handleSendMessage();
        }
    };

    return (
        <div className="flex min-h-screen bg-background text-foreground">

            {/* Sidebar */}
            <aside className="hidden w-64 flex-col border-r border-border bg-card/40 md:flex">

                <div className="flex h-16 items-center gap-3 border-b border-border px-5">
                    <div className="flex h-8 w-8 items-center justify-center rounded-lg bg-secondary">
                        <Bot className="h-4 w-4 text-zinc-200" />
                    </div>

                    <span className="font-semibold tracking-tight">
                        LocalAI
                    </span>
                </div>

                <div className="flex-1 p-4">

                    <p className="mb-3 px-2 text-xs font-medium uppercase tracking-wider text-muted-foreground">
                        Workspace
                    </p>

                    <div className="rounded-lg bg-secondary/70 border border-border/60 px-3 py-3">
                        <div className="flex items-center gap-3">

                            <Database className="h-4 w-4 text-zinc-300" />

                            <div>
                                <p className="text-sm font-medium">
                                    Restaurant
                                </p>

                                <p className="text-xs text-muted-foreground">
                                    MySQL database
                                </p>
                            </div>

                        </div>
                    </div>

                </div>

                <div className="border-t border-border p-4">
                    <Button
                        variant="ghost"
                        className="w-full justify-start text-muted-foreground hover:text-foreground"
                    >
                        <Settings className="mr-2 h-4 w-4" />
                        Settings
                    </Button>
                </div>

            </aside>

            {/* Main */}
            <main className="flex min-w-0 flex-1 flex-col">

                {/* Header */}
                <header className="flex h-16 items-center justify-between border-b border-border bg-background/90 px-4 md:px-6 backdrop-blur-md">

                    <div className="flex items-center gap-3">

                        <Button
                            variant="ghost"
                            size="icon"
                            className="md:hidden text-muted-foreground"
                        >
                            <Menu className="h-5 w-5" />
                        </Button>

                        <div>
                            <h1 className="text-sm font-semibold tracking-tight">
                                Restaurant AI
                            </h1>

                            <div className="mt-0.5 flex items-center gap-2">

                                <span className="h-1.5 w-1.5 rounded-full bg-emerald-400" />

                                <span className="text-xs text-muted-foreground">
                                    Connected
                                </span>

                            </div>
                        </div>

                    </div>

                    <Badge className="border-emerald-400/20 bg-emerald-400/10 text-emerald-300">
                        Local
                    </Badge>

                </header>

                {/* Chat area */}
                <div className="flex flex-1 flex-col overflow-hidden">

                    <div className="mx-auto flex w-full max-w-4xl flex-1 flex-col overflow-y-auto px-4 py-8 md:px-8">

                        {/* Welcome */}
                        <div className="mb-10 text-center">

                            <div className="mx-auto mb-4 flex h-12 w-12 items-center justify-center rounded-xl border border-border bg-secondary">
                                <Bot className="h-6 w-6 text-zinc-200" />
                            </div>

                            <h2 className="text-2xl font-semibold tracking-tight">
                                Restaurant Assistant
                            </h2>

                            <p className="mt-2 text-sm text-muted-foreground">
                                Ask questions about your live restaurant data.
                            </p>

                        </div>

                        {/* Messages Stream */}
                        <div className="flex flex-col space-y-4">
                            {messages.map((msg, index) => {
                                const isUser = msg.sender === "user" || msg.role === "user";
                                const messageText = msg.text || msg.content;
                                const messageKey = msg.id || `msg-${index}`;

                                return isUser ? (
                                    <div key={messageKey} className="flex justify-end">
                                        <div className="max-w-[80%] rounded-2xl rounded-br-md bg-primary px-4 py-3 text-sm text-primary-foreground font-normal">
                                            {messageText}
                                        </div>
                                    </div>
                                ) : (
                                    <div key={messageKey} className="flex gap-3">
                                        <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border border-border bg-secondary">
                                            <Bot className="h-4 w-4 text-zinc-200" />
                                        </div>

                                        <div className="max-w-[80%] rounded-2xl rounded-tl-md border border-border bg-card px-5 py-4 text-sm text-card-foreground">
                                            {messageText}
                                        </div>
                                    </div>
                                );
                            })}

                            {isLoading && (

                                <div className="flex gap-3 animate-pulse">
                                    <div className="flex h-8 w-8 shrink-0 items-center justify-center rounded-lg border border-border bg-secondary">
                                        <Bot className="h-4 w-4 text-zinc-200" />
                                    </div>

                                    <div className="max-w-[80%] rounded-2xl rounded-tl-md border border-border bg-card px-5 py-4 text-sm text-muted-foreground flex items-center gap-2">
                                        <span className="inline-block h-2 w-2 rounded-full bg-zinc-400 animate-bounce [animation-delay:-0.3s]"></span>
                                        <span className="inline-block h-2 w-2 rounded-full bg-zinc-400 animate-bounce [animation-delay:-0.15s]"></span>
                                        <span className="inline-block h-2 w-2 rounded-full bg-zinc-400 animate-bounce"></span>
                                        <span className="ml-2 text-xs">Querying database with SQL Agent...</span>
                                    </div>
                                </div>
                            )}
                            <div ref={messagesEndRef} />
                        </div>

                    </div>

                    {/* Input */}
                    <div className="border-t border-border bg-background/90 p-4 backdrop-blur-xl">

                        <div className="mx-auto flex max-w-4xl items-center gap-2 rounded-xl border border-border bg-card p-2 shadow-lg shadow-black/40">

                            <Input
                                placeholder="Ask anything about your database..."
                                value={inputQuery}
                                onChange={(e) => setInputQuery(e.target.value)}
                                onKeyDown={handleKeyDown}
                                disabled={isLoading}
                                className="border-0 bg-transparent shadow-none focus-visible:ring-0 text-foreground placeholder:text-muted-foreground disabled:opacity-50"
                            />

                            <Button
                                size="icon"
                                onClick={handleSendMessage}
                                disabled={!inputQuery.trim() || isLoading}
                                className="h-9 w-9 shrink-0 rounded-lg bg-primary text-primary-foreground hover:bg-primary/90 disabled:opacity-40"
                            >
                                <Send className="h-4 w-4" />
                            </Button>

                        </div>

                        <p className="mx-auto mt-2 max-w-4xl text-center text-[11px] text-muted-foreground">
                            LocalAI uses your configured data sources to answer questions.
                        </p>

                    </div>

                </div>

            </main>
        </div>
    );
}
