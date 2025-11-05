import { useState } from "react";
import {
  Box,
  VStack,
  HStack,
  Input,
  Button,
  Text,
  Heading,
  Select,
  Textarea,
  useToast,
  Spinner,
} from "@chakra-ui/react";
import { chatWithAI } from "../../api/ai";

export default function AIChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [systemPrompt, setSystemPrompt] = useState("");
  const [presetPrompt, setPresetPrompt] = useState("");
  const [temperature, setTemperature] = useState(0.5);
  const toast = useToast();

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMessage = { role: "user", content: input };
    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setInput("");

    try {
      setLoading(true);
      const payload = {
        messages: updatedMessages,
        model: "command-a-03-2025",
        temperature: temperature,
        system_prompt: systemPrompt || undefined,
        preset_prompt: presetPrompt || undefined,
      };

      const res = await chatWithAI(payload);
      const aiMessage = { role: "assistant", content: res.response || "No response." };
      setMessages((prev) => [...prev, aiMessage]);
    } catch (err) {
      console.error(err);
      toast({
        title: "Error fetching AI response",
        status: "error",
        duration: 3000,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box maxW="800px" mx="auto" mt={10} p={4}>
      <VStack spacing={4} align="stretch">
        <Heading size="md" textAlign="center">
          💬 AI Chat Interface
        </Heading>

        {/* Optional System and Preset Prompts */}
        <Textarea
          placeholder="System Prompt (optional)"
          value={systemPrompt}
          onChange={(e) => setSystemPrompt(e.target.value)}
        />
        <Input
          placeholder="Preset Prompt (optional)"
          value={presetPrompt}
          onChange={(e) => setPresetPrompt(e.target.value)}
        />

        <Select
          value={temperature}
          onChange={(e) => setTemperature(parseFloat(e.target.value))}
        >
          <option value={0}>0 (Deterministic)</option>
          <option value={0.3}>0.3</option>
          <option value={0.5}>0.5 (Balanced)</option>
          <option value={0.7}>0.7</option>
          <option value={1}>1 (Creative)</option>
        </Select>

        {/* Chat window */}
        <Box
          borderWidth="1px"
          borderRadius="md"
          p={4}
          height="400px"
          overflowY="auto"
          bg="gray.50"
        >
          {messages.length === 0 ? (
            <Text color="gray.500" textAlign="center">
              Start chatting with the AI...
            </Text>
          ) : (
            messages.map((msg, idx) => (
              <Box
                key={idx}
                textAlign={msg.role === "user" ? "right" : "left"}
                mb={3}
              >
                <Box
                  display="inline-block"
                  bg={msg.role === "user" ? "blue.100" : "green.100"}
                  px={3}
                  py={2}
                  borderRadius="lg"
                >
                  <Text>{msg.content}</Text>
                </Box>
              </Box>
            ))
          )}
          {loading && (
            <Box textAlign="center" mt={2}>
              <Spinner size="sm" />
            </Box>
          )}
        </Box>

        {/* Message input */}
        <HStack>
          <Input
            placeholder="Type your message..."
            value={input}
            onChange={(e) => setInput(e.target.value)}
            onKeyDown={(e) => e.key === "Enter" && handleSend()}
          />
          <Button colorScheme="blue" onClick={handleSend} isDisabled={loading}>
            Send
          </Button>
        </HStack>
      </VStack>
    </Box>
  );
}
