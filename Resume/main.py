import tkinter as tk
from tkinter import ttk
import webbrowser
from PIL import Image, ImageTk 
import os 

class ResumeApp:
    def __init__(self, master):
        self.master = master
        master.title("Curriculum Vitae")
        master.geometry("400x700") 
        master.resizable(True, True) 

        self.experience_images = {} 

        # --- Styling & Colors ---
        s = ttk.Style()
        s.theme_use('clam') 
        
        # General colors
        self.bg_color = "#f8f9fa"       
        self.primary_color = "#800000"  # MAROON
        self.text_color = "#000000"     # BLACK
        self.light_text_color = "#444444" 
        self.border_color = "#dddddd"   
        self.tag_bg = "#f0f0f0"         
        self.button_bg_light = "#add8e6" # Light blue for project buttons
        self.button_fg_dark = "#000080"  # Dark blue for button text

        master.configure(bg=self.bg_color)
        s.configure('TFrame', background=self.bg_color)
        s.configure('TLabel', background=self.bg_color, foreground=self.text_color)
        
        # --- Custom Font Styles ---
        s.configure('Title.TLabel', font=('Arial', 14, 'bold'), foreground=self.text_color)
        s.configure('Header.TLabel', font=('Arial', 15, 'bold'), foreground=self.text_color) 
        s.configure('Subtitle.TLabel', font=('Arial', 10), foreground=self.primary_color)
        s.configure('Body.TLabel', font=('Arial', 9), foreground=self.text_color)
        s.configure('LightBody.TLabel', font=('Arial', 9), foreground=self.light_text_color)

        s.configure('WhiteBackground.TFrame', background='white', relief='flat', borderwidth=0)
        s.configure('WhiteBackground.TLabel', background='white', foreground=self.text_color)
        
        # New style for Project Cards
        s.configure('Project.TFrame', background='#f0f0f0', borderwidth=1, relief='solid')
        s.configure('Project.TLabel', background='#f0f0f0', foreground=self.text_color)

        # NEW: Style for Experience Image Container
        s.configure('ExperienceImage.TFrame', background='#f0f0f0', borderwidth=1, relief='solid', padding=10) # Gray background for container
        s.configure('ExperienceImage.TLabel', background='#f0f0f0') # Match label background to container


        # Standard button (used for LinkedIn/GitHub in header)
        s.configure('TButton', font=('Arial', 10, 'bold'), foreground='white', background=self.primary_color,
                    padding=10, relief='flat', borderwidth=0)
        s.map('TButton', background=[('active', '#660000')]) 

        # New style for Secondary button (GitHub)
        s.configure('Secondary.TButton', font=('Arial', 10), foreground=self.primary_color, background=self.tag_bg,
                    padding=10, relief='flat', borderwidth=0)
        s.map('Secondary.TButton', background=[('active', self.border_color)])


        # Project button style (for use in the Projects tab)
        s.configure('Project.TButton', font=('Arial', 9), foreground=self.button_fg_dark, background=self.button_bg_light,
                    relief='flat', borderwidth=0, padding=(5, 5))
        s.map('Project.TButton', background=[('active', '#aed5e2')])


        s.configure('Tab.TButton', background=self.bg_color, foreground=self.text_color, font=('Arial', 10),
                    relief='flat', padding=(10, 5))
        s.map('Tab.TButton',
              background=[('pressed', self.primary_color), ('active', self.border_color)],
              foreground=[('pressed', 'white'), ('active', self.text_color)],
              font=[('pressed', ('Arial', 10, 'bold'))]) 
        
        s.configure('Tag.TLabel', background=self.tag_bg, foreground=self.text_color, font=('Arial', 8), padding=5)

        self.create_widgets()

    # --- Utility function to open links ---
    def open_link(self, url):
        webbrowser.open_new(url)

    # --- Load and Prepare Profile Photo (100x100) ---
    def load_photo(self):
        try:
            original_image = Image.open("my_photo.png") 
            size = (100, 100) 
            resized_image = original_image.resize(size, Image.Resampling.LANCZOS)
            self.photo_img = ImageTk.PhotoImage(resized_image)
            return self.photo_img
        except FileNotFoundError:
            print("Error: 'my_photo.png' not found. Displaying initials instead.")
            return None
        except Exception as e:
            print(f"An error occurred while loading the profile image: {e}")
            return None
            
    # --- UPDATED: Load and Prepare Experience Images (250x150) ---
    def load_experience_image(self, file_name, width=250, height=150): # Increased size
        try:
            if not os.path.exists(file_name):
                 print(f"Warning: Experience image '{file_name}' not found.")
                 return ImageTk.PhotoImage(Image.new('RGB', (width, height), color='lightgray'))
                 
            original_image = Image.open(file_name) 
            size = (width, height) 
            resized_image = original_image.resize(size, Image.Resampling.LANCZOS)
            
            self.experience_images[file_name] = ImageTk.PhotoImage(resized_image)
            return self.experience_images[file_name]
            
        except Exception as e:
            print(f"An error occurred while loading experience image '{file_name}': {e}")
            return None

    def create_widgets(self):
        # --- Top Bar Frame ---
        top_bar_frame = ttk.Frame(self.master, padding=(20, 10))
        top_bar_frame.pack(fill='x')
        ttk.Label(top_bar_frame, text="Curriculum Vitae", style='Title.TLabel').pack(side='left')
        ttk.Label(top_bar_frame, text="⬇", font=("Arial", 14), foreground=self.light_text_color).pack(side='right')

        # --- Profile Header Frame (The White Card) ---
        header_frame = ttk.Frame(self.master, padding=(20, 15), style='WhiteBackground.TFrame')
        header_frame.pack(fill='x', pady=(0, 10), padx=20) 

        # --- PHOTO INTEGRATION / FALLBACK ---
        photo = self.load_photo()
        if photo:
            photo_label = ttk.Label(header_frame, image=photo, background='white')
            photo_label.pack(side='left', padx=(0, 15), ipadx=0, ipady=0)
            photo_label.image = photo 
        else:
            jd_label = ttk.Label(header_frame, text="AP", background=self.primary_color, foreground="white",
                                 font=("Arial", 20, "bold"), anchor="center")
            jd_label.pack(side='left', padx=(0, 15), ipadx=10, ipady=10)
            jd_label.configure(width=1) 


        info_frame = ttk.Frame(header_frame, style='WhiteBackground.TFrame')
        info_frame.pack(side='left', fill='x', expand=True) 

        # Name 
        ttk.Label(info_frame, text="Aiko Lindsay J. Pahuyo", style='Header.TLabel', background='white').pack(anchor='w')
        
        ttk.Label(info_frame, text="Computer Science Student", style='Subtitle.TLabel', background='white').pack(anchor='w')

        bio_text = """Passionate student developer seeking opportunities to apply foundational knowledge in full-stack development. Proficient in modern programming languages and collaborative development tools."""
        
        ttk.Label(info_frame, text=bio_text, wraplength=320, style='LightBody.TLabel', background='white', justify='left').pack(anchor='w', pady=(5, 10))

        # --- Connect buttons Frame (CENTERED) ---
        button_frame = ttk.Frame(self.master, style='TFrame')
        button_frame.pack(pady=(0, 15), padx=20, fill='x') 
        
        inner_button_frame = ttk.Frame(button_frame, style='TFrame')
        inner_button_frame.pack(anchor='center') 

        # 1. LinkedIn Button (Primary)
        linkedin_button = ttk.Button(
            inner_button_frame, 
            text="Connect on LinkedIn", 
            style='TButton',
            command=lambda: self.open_link("https://www.linkedin.com/in/aiko-pahuyo-196191373/") 
        )
        linkedin_button.pack(side='left', padx=(0, 10)) 

        # 2. GitHub Button (Secondary)
        github_button = ttk.Button(
            inner_button_frame, 
            text="GitHub", 
            style='Secondary.TButton',
            command=lambda: self.open_link("https://github.com/misuuwu") 
        )
        github_button.pack(side='left') 

        # --- Tab Navigation Frame ---
        tab_nav_frame = ttk.Frame(self.master, padding=(20, 0), style='WhiteBackground.TFrame')
        tab_nav_frame.pack(fill='x', pady=(0, 10), padx=20) 

        self.tab_buttons = []
        tab_names = ["Experience", "Projects", "Skills", "Education"]

        for tab_name in tab_names:
            btn = ttk.Button(tab_nav_frame, text=tab_name, style='Tab.TButton',
                             command=lambda name=tab_name: self.show_tab(name))
            btn.pack(side='left', expand=True, fill='x', padx=2, pady=5)
            self.tab_buttons.append(btn)


        # --- Content Area ---
        self.content_container_frame = ttk.Frame(self.master, padding=20, style='WhiteBackground.TFrame')
        self.content_container_frame.pack(fill='both', expand=True, padx=20, pady=(0, 20)) 

        self.experience_frame = self.create_experience_tab(self.content_container_frame)
        self.projects_frame = self.create_projects_tab(self.content_container_frame) 
        self.skills_frame = self.create_skills_tab(self.content_container_frame)
        self.education_frame = self.create_education_tab(self.content_container_frame)

        self.show_tab("Experience")

    def show_tab(self, tab_name):
        # Hide all tab frames
        for frame in [self.experience_frame, self.projects_frame, self.skills_frame, self.education_frame]:
            frame.pack_forget()

        # Show the selected tab frame
        if tab_name == "Experience":
            self.experience_frame.pack(fill='both', expand=True)
        elif tab_name == "Projects":
            self.projects_frame.pack(fill='both', expand=True)
        elif tab_name == "Skills":
            self.skills_frame.pack(fill='both', expand=True)
        elif tab_name == "Education":
            self.education_frame.pack(fill='both', expand=True)

        # Update button styles
        for btn in self.tab_buttons:
            if btn.cget('text') == tab_name:
                btn.state(['pressed'])
            else:
                btn.state(['!pressed'])

    # --- Project Card Creation Helper (Used in Projects Tab) ---
    def create_project_card(self, parent_frame, title, description, repo_link):
        card_frame = ttk.Frame(parent_frame, style='Project.TFrame', padding=10)
        card_frame.pack(fill='x', pady=5)

        ttk.Label(card_frame, text=title, font=('Arial', 10, 'bold'), style='Project.TLabel').pack(anchor='w')
        ttk.Label(card_frame, text=description, wraplength=300, style='LightBody.TLabel', background='#f0f0f0', justify='left').pack(anchor='w', pady=(5, 10))

        ttk.Button(card_frame, text="<> View Repository", style='Project.TButton', 
                   command=lambda: self.open_link(repo_link)).pack(anchor='w')
        return card_frame

    # --- UPDATED: Experience Tab Content with Larger Images in Gray Container ---
    def create_experience_tab(self, parent_frame):
        frame = ttk.Frame(parent_frame, style='WhiteBackground.TFrame')
        
        ttk.Label(frame, text="Full-Stack E-commerce Platform", style='Title.TLabel', background='white').pack(anchor='w')
        ttk.Label(frame, text="Personal Project / Capstone | Sept 2023 - Present", style='LightBody.TLabel', background='white').pack(anchor='w', pady=(0,5))
        
        # Bullet Points
        ttk.Label(frame, text="• Developed a responsive e-commerce site using \"React, Node.js, and MongoDB\"", style='Body.TLabel', background='white', wraplength=320, justify='left').pack(anchor='w', pady=(2,0))
        ttk.Label(frame, text="• Implemented user authentication, product catalog management, and secure payment processing.", style='Body.TLabel', background='white', wraplength=320, justify='left').pack(anchor='w', pady=(2,0))
        ttk.Label(frame, text="• Utilized \"Tailwind CSS\" for modern UI/UX design.", style='Body.TLabel', background='white', wraplength=320, justify='left').pack(anchor='w', pady=(2,10))
        
        # --- Image Showcase Section with Gray Container ---
        ttk.Label(frame, text="Project Visuals", style='Subtitle.TLabel', foreground=self.primary_color, background='white').pack(anchor='w', pady=(10, 5))
        
        # Main container for images with gray background and padding
        image_container_frame = ttk.Frame(frame, style='ExperienceImage.TFrame')
        image_container_frame.pack(fill='x', pady=(0, 10)) # Adjust padding as needed
        
        # Inner frame to hold images side-by-side, centered within the container
        inner_image_frame = ttk.Frame(image_container_frame, style='ExperienceImage.TFrame')
        inner_image_frame.pack(anchor='center', expand=True) # Center the inner frame
        
        # 1. E-commerce Image (250x150)
        ecommerce_img = self.load_experience_image("ecommerce_project.png", width=250, height=150) 
        if ecommerce_img:
            ttk.Label(inner_image_frame, image=ecommerce_img, style='ExperienceImage.TLabel').pack(side='left', padx=5, pady=5)

        # 2. Flutter Image (250x150)
        flutter_img = self.load_experience_image("flutter_project.png", width=250, height=150) 
        if flutter_img:
            ttk.Label(inner_image_frame, image=flutter_img, style='ExperienceImage.TLabel').pack(side='left', padx=5, pady=5)
            
        # 3. Blender Image (250x150)
        blender_img = self.load_experience_image("blender_project.png", width=250, height=150) 
        if blender_img:
            ttk.Label(inner_image_frame, image=blender_img, style='ExperienceImage.TLabel').pack(side='left', padx=5, pady=5)

        return frame

    # --- Projects Tab Content (Unchanged) ---
    def create_projects_tab(self, parent_frame):
        frame = ttk.Frame(parent_frame, style='WhiteBackground.TFrame')
        
        ttk.Label(frame, text="My Featured Projects", style='Title.TLabel', background='white').pack(anchor='w', pady=(0,10))

        # E-Commerce Platform
        self.create_project_card(
            frame,
            title="E-Commerce Platform (HTML, CSS, and JavaScript)",
            description="A fully functional mobile e-commerce application built with HTML, CSS, and JavaScript, showcasing clean architecture and smooth animations.",
            repo_link="https://github.com/misuuwu/Ecommerce-API"
        )
        
        # Expense-Tracker
        self.create_project_card(
            frame,
            title="Expense-Tracker",
            description="My personal Expense-Tracker built with React and TypeScript, demonstrating responsive design, modern hooks, and state management.",
            repo_link="https://github.com/Pragmatyst/Expense-Tracker"
        )
        
        # Flashwise V1
        self.create_project_card(
            frame,
            title="Flashwise V1",
            description="Your electrifying new study sidekick that zaps away boredom and supercharges your brain!",
            repo_link="https://github.com/misuuwu/Flashwise_V1"
        )
        
        return frame


    # --- Skills Tab Content (Unchanged) ---
    def create_skills_tab(self, parent_frame):
        frame = ttk.Frame(parent_frame, style='WhiteBackground.TFrame')
        
        # --- Programming Languages Section ---
        ttk.Label(frame, text="<> Programming Languages", style='Title.TLabel', background='white').pack(anchor='w', pady=(0,5))
        
        # Skill Tags Frame
        skill_tag_frame_1 = ttk.Frame(frame, style='WhiteBackground.TFrame')
        skill_tag_frame_1.pack(fill='x', anchor='w', pady=(0, 5))
        
        # Skill tags use the 'Tag.TLabel' style for a boxed look
        ttk.Label(skill_tag_frame_1, text="Python (Advanced)", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        ttk.Label(skill_tag_frame_1, text="JavaScript (ES6+)", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        ttk.Label(skill_tag_frame_1, text="Java", style='Tag.TLabel').pack(side='left', padx=(0, 5))

        skill_tag_frame_2 = ttk.Frame(frame, style='WhiteBackground.TFrame')
        skill_tag_frame_2.pack(fill='x', anchor='w', pady=(0, 15))
        ttk.Label(skill_tag_frame_2, text="C++", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        ttk.Label(skill_tag_frame_2, text="SQL / MySQL", style='Tag.TLabel').pack(side='left', padx=(0, 5))


        # --- Frontend Development Section ---
        ttk.Label(frame, text=" Frontend Development", style='Title.TLabel', background='white').pack(anchor='w', pady=(0,5))

        # Frontend Tags Frame
        frontend_tag_frame_1 = ttk.Frame(frame, style='WhiteBackground.TFrame')
        frontend_tag_frame_1.pack(fill='x', anchor='w', pady=(0, 5))
        
        ttk.Label(frontend_tag_frame_1, text="React", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        ttk.Label(frontend_tag_frame_1, text="Next.js (Basics)", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        ttk.Label(frontend_tag_frame_1, text="Tailwind CSS", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        
        ttk.Label(frame, text="Responsive Design", style='Tag.TLabel').pack(anchor='w', pady=(0, 5))

        return frame

    # --- Education Tab Content (Unchanged) ---
    def create_education_tab(self, parent_frame):
        frame = ttk.Frame(parent_frame, style='WhiteBackground.TFrame')
        
        # Degree/GPA
        degree_frame = ttk.Frame(frame, style='WhiteBackground.TFrame')
        degree_frame.pack(fill='x', pady=(0, 5))
        
        # Course
        ttk.Label(degree_frame, text="Technical Vocation Major in Computer Harwdare Servicing", style='Title.TLabel', background='white').pack(side='left', anchor='w')
        # GPA box uses Maroon background
        ttk.Label(degree_frame, text="3.9 GPA", font=("Arial", 9, "bold"), background=self.primary_color, foreground="white").pack(side='right', padx=5, ipady=3) 

        # School
        ttk.Label(frame, text="Technological University of the Philippines", style='Body.TLabel', background='white').pack(anchor='w')
        ttk.Label(frame, text="Major in Software Development | Expected May 2026", style='LightBody.TLabel', background='white').pack(anchor='w', pady=(0,15))

        # Key Coursework
        ttk.Label(frame, text="Key Coursework:", style='Title.TLabel', background='white').pack(anchor='w', pady=(0,5))
        
        # Coursework Tags (Use Tag.TLabel style)
        course_tag_frame_1 = ttk.Frame(frame, style='WhiteBackground.TFrame')
        course_tag_frame_1.pack(fill='x', anchor='w', pady=(0, 5))
        
        ttk.Label(course_tag_frame_1, text="Data Structures", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        ttk.Label(course_tag_frame_1, text="Algorithms & Analysis", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        
        course_tag_frame_2 = ttk.Frame(frame, style='WhiteBackground.TFrame')
        course_tag_frame_2.pack(fill='x', anchor='w', pady=(0, 5))
        
        ttk.Label(course_tag_frame_2, text="Operating Systems", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        ttk.Label(course_tag_frame_2, text="Database Systems", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        
        course_tag_frame_3 = ttk.Frame(frame, style='WhiteBackground.TFrame')
        course_tag_frame_3.pack(fill='x', anchor='w', pady=(0, 5))
        ttk.Label(course_tag_frame_3, text="Full-Stack Web Dev", style='Tag.TLabel').pack(side='left', padx=(0, 5))
        
        return frame


if __name__ == "__main__":
    root = tk.Tk()
    app = ResumeApp(root)
    root.mainloop()