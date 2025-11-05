import { useState } from "react";
import { Box, Heading, VStack, Button, Input, useToast } from "@chakra-ui/react";
import { uploadFileTask } from "../../api/tasks";

export default function UploadTask() {
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const toast = useToast();

  const handleUpload = async (e) => {
    e.preventDefault();

    if (!file) {
      toast({
        title: "No file selected",
        status: "warning",
        duration: 3000,
        isClosable: true,
      });
      return;
    }

    setLoading(true);
    try {
      const result = await uploadFileTask(file);

      toast({
        title: "File Uploaded!",
        description: result.message || "Upload successful.",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
      setFile(null);
    } catch (err) {
      toast({
        title: "Upload failed",
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
      <Heading size="lg" mb={4}>Upload File Task</Heading>
      <form onSubmit={handleUpload}>
        <VStack spacing={4}>
          <Input type="file" onChange={(e) => setFile(e.target.files[0])} />
          <Button colorScheme="teal" type="submit" isLoading={loading} w="full">
            Upload File
          </Button>
        </VStack>
      </form>
    </Box>
  );
}
