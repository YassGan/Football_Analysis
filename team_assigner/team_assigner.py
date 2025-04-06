from sklearn.cluster import KMeans

class TeamAssigner:
    def __init__(self):
        self.team_colors={}
        self.player_team_dict={}


    def get_clustering_model(self, image):
        # reshape the image to a 2D array of pixels
        image_2d=image.reshape((-1,3))
        # perform k-means clustering
        kmeans = KMeans(n_clusters=2,init="k-means++", n_init=1 ,random_state=0)
        kmeans.fit(image_2d)
        return kmeans


    def get_player_color(self,frame,bbox):
        image=frame[int(bbox[1]):int(bbox[3]), int(bbox[0]):int(bbox[2])]
        top_half_image = image[0:int(image.shape[0]/2),:]
        kmeans=self.get_clustering_model(top_half_image)
        
        # Get the labels for each pixel
        labels = kmeans.labels_
        # reshape the labels to match the original image shape
        clustered_image = labels.reshape(top_half_image.shape[0], top_half_image.shape[1])
        # get the player cluster
        corner_clusters=[clustered_image[0][0],clustered_image[0][-1],clustered_image[-1][0],clustered_image[-1][-1]]
        non_player_cluster=max(set(corner_clusters),key=corner_clusters.count)
        player_cluster=1-non_player_cluster
        player_color=kmeans.cluster_centers_[player_cluster]
        print(f"Bbox {bbox}: Player color={player_color}")
        return player_color



    def assign_teams(self, frame, player_detections):

        player_colors=[]
        for _, player_detection in player_detections.items():
            # Extract the bounding box coordinates
            bbox = player_detection['bbox']
            player_color= self.get_player_color(frame, bbox)
            player_colors.append(player_color)

        kmeans=KMeans(n_clusters=2,init="k-means++", n_init=1 ,random_state=0)
        kmeans.fit(player_colors)

        self.kmeans=kmeans

        self.team_colors[1]=kmeans.cluster_centers_[0]
        self.team_colors[2]=kmeans.cluster_centers_[1]

        print("Team 1 color:", self.team_colors[1])
        print("Team 2 color:", self.team_colors[2])


    def get_player_team(self, frame, player_bbox, player_id):
        if player_id in self.player_team_dict:
            return self.player_team_dict[player_id]
        
        player_color=self.get_player_color(frame, player_bbox)

        team_id=self.kmeans.predict(player_color.reshape(1,-1))[0]
        team_id+=1

        print(f"Player {player_id}: Color={player_color}, Predicted Team={team_id}")

        self.player_team_dict[player_id]=team_id
        return team_id
