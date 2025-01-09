import { ref, computed } from "vue";

export interface Course {
  id: number;
  name: string;
  groupCount: number;
}

const courses = ref<Course[]>([
  { id: 1, name: "Math 101", groupCount: 3 },
  { id: 2, name: "Physics 202", groupCount: 2 },
  { id: 3, name: "Chemistry 303", groupCount: 5 },
  { id: 4, name: "Biology 404", groupCount: 1 },
  { id: 5, name: "English 505", groupCount: 4 },
]);

const isLoading = ref(false);
const isError = ref(false);

const professorCourses = ref<number[]>([1, 2, 3]); // IDs of courses the professor has access to.

export function useCourses() {
  const filterCourses = (search: string) => {
    if (!search) return courses.value.filter(isEligible);
    return courses.value.filter(
      (course) =>
        isEligible(course) &&
        course.name.toLowerCase().includes(search.toLowerCase()),
    );
  };

  async function getAllStats() {
    try {
      // await ensureAuthenticated();
      isError.value = false;
      isLoading.value = true;
      const response = await useApiFetch("/courses/all_stats", {
        method: "GET",
      });
      return response;
    } catch (error) {
      isError.value = true;
      throw error;
    } finally {
      isLoading.value = false;
    }
  }

  const isEligible = (course: Course) =>
    professorCourses.value.includes(course.id);

  return {
    courses: computed(() => courses.value.filter(isEligible)),
    filterCourses,
    isEligible,
    getAllStats,
  };
}
