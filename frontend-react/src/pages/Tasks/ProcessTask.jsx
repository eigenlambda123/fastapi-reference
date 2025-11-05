// src/pages/tasks/ProcessTask.jsx
import { useState } from "react";
import { Box, Heading, VStack, Button, Textarea, useToast } from "@chakra-ui/react";
import { runBackgroundTask } from "../../api/tasks";

export default function ProcessTask() {
  const [taskData, setTaskData] = useState("");
  const [loading, setLoading] = useState(false);
  const toast = useToast();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);

    try {
      const payload = { data: taskData };
      const result = await runBackgroundTask(payload);

      toast({
        title: "Task Submitted!",
        description: result.message || "Background task started.",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
      setTaskData("");
    } catch (err) {
      toast({
        title: "Error Running Task",
        description: err.response?.data?.detail || err.message,
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box maxW="lg" mx="auto" mt={10} p={6} borderWidth="1px" borderRadius="2xl" boxShadow="md">
      <Heading size="lg" mb={4}>Run Background Task</Heading>
      <form onSubmit={handleSubmit}>
        <VStack spacing={4}>
          <Textarea
            placeholder="Enter task data (JSON, text, etc.)"
            value={taskData}
            onChange={(e) => setTaskData(e.target.value)}
            size="md"
          />
          <Button colorScheme="blue" type="submit" isLoading={loading} w="full">
            Run Task
          </Button>
        </VStack>
      </form>
    </Box>
  );
}
