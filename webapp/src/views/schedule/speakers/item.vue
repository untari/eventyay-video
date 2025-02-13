<template lang="pug">
.c-schedule-speaker
	bunt-progress-circular(v-if="!speaker || !schedule", size="huge", :page="true")
	scrollbars(v-else, y="")
		.profile
			img.avatar(v-if="speaker.avatar", :src="speaker.avatar")
			identicon(v-else, :user="{id: speaker.name, profile: {display_name: speaker.name}}")
			.content
				h1 {{ speaker.name }}
				markdown-content.biography(:markdown="speaker.biography")
		.sessions
			h2 {{ $t('schedule/speakers/item:sessions:header') }}
			session(
				v-for="session of sessions",
				:session="session",
				:faved="favs.includes(session.id)",
				@fav="$store.dispatch('schedule/fav', $event)",
				@unfav="$store.dispatch('schedule/unfav', $event)"
			)
</template>
<script>
import { mapState, mapGetters } from 'vuex'
import Identicon from 'components/Identicon'
import MarkdownContent from 'components/MarkdownContent'
import { Session } from '@pretalx/schedule'

export default {
	components: { Identicon, MarkdownContent, Session },
	props: {
		speakerId: String
	},
	data() {
		return {
			speaker: null
		}
	},
	provide() {
		return {
			generateSessionLinkUrl: this.generateSessionLinkUrl
		}
	},
	computed: {
		...mapState('schedule', ['schedule']),
		...mapGetters('schedule', ['sessionsLookup', 'favs']),
		sessions() {
			if (this.speaker.submissions) {
				return this.speaker.submissions
					.map(submission => this.sessionsLookup[submission])
					.filter(session => session !== undefined)
			}
			return this.$store.getters['schedule/sessions'].filter(session => session.speakers.includes(this.speaker))
		}
	},
	async created() {
		// TODO error handling
		if (this.$store.getters['schedule/pretalxApiBaseUrl']) {
			this.speaker = await (await fetch(`${this.$store.getters['schedule/pretalxApiBaseUrl']}/speakers/${this.speakerId}/`)).json()
		} else {
			this.$watch('schedule', (schedule) => {
				if (!schedule) return
				this.speaker = schedule.speakers.find(speaker => speaker.id === this.speakerId || speaker.code === this.speakerId)
			}, { immediate: true })
		}
	},
	mounted() {},
	methods: {
		generateSessionLinkUrl(sessionData) {
			const publicPath = process.env.BASE_URL || '/video/'
			return `${publicPath}schedule/talks/${sessionData.session.id}`
		}
	}
}
</script>
<style lang="stylus">
.c-schedule-speaker
	display: flex
	background-color: $clr-white
	flex-direction: column
	min-height: 0
	.c-scrollbars
		.scroll-content
			display: flex
			flex-direction: column
			align-items: center
			> *
				width: @css{min(920px, 100%)}
	.speaker
		display: flex
		flex-direction: column
	.profile
		display: flex
		gap: 16px
		img
			border-radius: 50%
			height: 256px
			width: @height
			object-fit: cover
			padding: 16px
		h1
			margin: 24px 0 16px
		.content
			flex: auto
			margin-right: 16px
	.sessions
		h2
			margin: 16px
	+below('s')
		.profile
			flex-direction: column
			align-items: center
		.content
			margin: 0 16px
</style>
